from datetime import datetime, UTC, timedelta

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import db_connector, auth_config, settings, redis_db
from app.repositories import AuthRepository
from app.schemas import Tokens, GetMe


oauth_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.api_v1_prefix}/auth/login')

TYPE_ACCESS_TOKEN = "access"
TYPE_REFRESH_TOKEN = "refresh"


class AuthHelper:
    @staticmethod
    def get_hash_password(password: str) -> bytes:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    @staticmethod
    def validate_password(password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password)

    @staticmethod
    def encode_token(
            payload: dict,
            secret_key: str = auth_config.secret_key,
            algorithm: str = auth_config.algorithm
    ) -> str:
        return jwt.encode(payload, secret_key, algorithm)

    @staticmethod
    def decode_token(
            token: str | bytes,
            secret_key: str = auth_config.secret_key,
            algorithm: str = auth_config.algorithm
    ) -> dict:
        try:
            return jwt.decode(token, secret_key, algorithm)
        except jwt.InvalidTokenError:
            raise HTTPException(401)

    def authorize(self, token: str = Depends(oauth_scheme)) -> dict:
        data = self.decode_token(token)
        if data['type'] != TYPE_ACCESS_TOKEN:
            raise HTTPException(401)
        return data


class AuthService(AuthRepository, AuthHelper):

    def __init__(
            self,
            session: AsyncSession = Depends(db_connector.get_session),
            redis: Redis = Depends(redis_db.get_redis)
    ):
        self.session = session
        self.redis = redis

    def create_token(
            self,
            token_type: str,
            exp_time: timedelta,
            employee_id: int,
            employee_role_id: int
    ) -> str:
        exp = datetime.now(UTC) + exp_time
        payload = {
            "type": token_type,
            "exp": exp,
            "employee_id": employee_id,
            "role_id": employee_role_id
        }
        return self.encode_token(payload)

    async def validate_user(self, username: str, password: str, ip_address: str) -> Tokens:
        from_base = await self.get_user_by_login_for_auth(username, ip_address)
        if not from_base:
            raise HTTPException(401)
        employee, shop = from_base
        if not employee.is_active:
            raise HTTPException(403)
        if not self.validate_password(password, employee.password):
            raise HTTPException(401)
        access_token = self.create_token(
            TYPE_ACCESS_TOKEN,
            auth_config.access_token_exp,
            employee.id,
            employee.role_id)
        refresh_token = self.create_token(
            TYPE_REFRESH_TOKEN,
            auth_config.refresh_token_exp,
            employee.id,
            employee.role_id)
        await self.create_employee_cache(employee.id, shop, refresh_token)
        return Tokens(access_token=access_token, refresh_token=refresh_token)

    async def refresh_token(self, refresh_token: str) -> Tokens:
        payload = self.decode_token(refresh_token)
        if payload["type"] != TYPE_REFRESH_TOKEN:
            raise HTTPException(401)
        employee = await self.get_employee_cache(payload["employee_id"])
        if not employee:
            raise HTTPException(401)
        if employee.refresh_token != refresh_token:
            raise HTTPException(401)
        access_token = self.create_token(
            TYPE_ACCESS_TOKEN,
            auth_config.access_token_exp,
            payload["employee_id"],
            payload["role_id"])
        return Tokens(access_token=access_token)

    async def get_employee_info(self, payload_access: dict) -> GetMe:
        employee = await self.get_employee_cache(payload_access["employee_id"])
        if not employee:
            raise HTTPException(401)
        return GetMe(
            employee_id=payload_access["employee_id"],
            shop_id=employee.shop_id,
            role_id=payload_access["role_id"]
        )

    async def change_shop(self, employee_id: int, shop_id: int):
        employee = await self.update_employee_cache(employee_id, shop_id)
        if not employee:
            raise HTTPException(400, detail="неверный запрос")


class CheckRole(AuthHelper):

    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, data: dict = Depends(AuthHelper().authorize)):
        if data['role_id'] not in self.allowed_roles:
            raise HTTPException(status_code=403)
