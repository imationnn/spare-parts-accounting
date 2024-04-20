from datetime import datetime, UTC, timedelta

import bcrypt
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.config import auth_config, settings
from app.repositories import AuthRepository
from app.schemas import Tokens, GetMe
from app.exceptions import InvalidLoginPass, AccessIsDenied, InvalidToken, InvalidTokenType
from app.services import BaseService

oauth_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.api_v1_prefix}/auth/login')

TYPE_ACCESS_TOKEN = "access"
TYPE_REFRESH_TOKEN = "refresh"
NAME_FIELD_TYPE_TOKEN = "type"
NAME_FIELD_EXP = "exp"
NAME_FIELD_EMPLOYEE_ID = "employee_id"
NAME_FIELD_ROLE_ID = "role_id"


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
            raise InvalidToken

    @staticmethod
    def check_token_type(payload: dict, token_type: str) -> dict:
        if payload[NAME_FIELD_TYPE_TOKEN] != token_type:
            raise InvalidTokenType
        return payload

    @classmethod
    def authorize(cls, token: str = Depends(oauth_scheme)) -> dict:
        return cls.check_token_type(cls.decode_token(token), TYPE_ACCESS_TOKEN)


class AuthService(BaseService, AuthHelper):
    repository = AuthRepository()

    def create_token(
            self,
            token_type: str,
            exp_time: timedelta,
            employee_id: int,
            employee_role_id: int
    ) -> str:
        exp = datetime.now(UTC) + exp_time
        payload = {
            NAME_FIELD_TYPE_TOKEN: token_type,
            NAME_FIELD_EXP: exp,
            NAME_FIELD_EMPLOYEE_ID: employee_id,
            NAME_FIELD_ROLE_ID: employee_role_id
        }
        return self.encode_token(payload)

    async def validate_employee(self, username: str, password: str, ip_address: str) -> Tokens:
        """
        Takes username, password and ip address from request
        and returns access and refresh tokens in case of successful authentication.
        :param username:
        :param password:
        :param ip_address:
        :return:
        """
        from_base = await self.repository.get_user_by_login_for_auth(username, ip_address)
        if not from_base:
            raise InvalidLoginPass
        employee, shop = from_base
        if not employee.is_active:
            raise AccessIsDenied
        if not self.validate_password(password, employee.password):
            raise InvalidLoginPass
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
        await self.repository.create_employee_cache(employee.id, shop, refresh_token)
        return Tokens(access_token=access_token, refresh_token=refresh_token)

    async def refresh_token(self, refresh_token: str) -> Tokens:
        """
        Returns access token.
        :param refresh_token:
        :return:
        """
        payload = self.check_token_type(self.decode_token(refresh_token), TYPE_REFRESH_TOKEN)
        employee = await self.repository.get_employee_cache(payload[NAME_FIELD_EMPLOYEE_ID])
        if not employee:
            raise InvalidToken
        if employee.refresh_token != refresh_token:
            raise InvalidToken
        access_token = self.create_token(
            TYPE_ACCESS_TOKEN,
            auth_config.access_token_exp,
            payload[NAME_FIELD_EMPLOYEE_ID],
            payload[NAME_FIELD_ROLE_ID])
        return Tokens(access_token=access_token)

    async def get_employee_info(self, payload_access: dict) -> GetMe:
        """
        Takes data from access token and returns information about employee.
        :param payload_access:
        :return:
        """
        employee = await self.repository.get_employee_cache(payload_access[NAME_FIELD_EMPLOYEE_ID])
        if not employee:
            raise InvalidToken
        return GetMe(
            employee_id=payload_access[NAME_FIELD_EMPLOYEE_ID],
            shop_id=employee.shop_id,
            role_id=payload_access[NAME_FIELD_ROLE_ID]
        )

    async def change_shop(self, employee_id: int, shop_id: int):
        employee = await self.repository.update_employee_cache(employee_id, shop_id)
        if not employee:
            raise InvalidToken


class CheckRole:

    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, data: dict = Depends(AuthHelper.authorize)):
        if data[NAME_FIELD_ROLE_ID] not in self.allowed_roles:
            raise AccessIsDenied
        return data
