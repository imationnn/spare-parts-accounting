from fastapi import APIRouter, Depends, Form, Request

from app.models import Roles
from app.services import AuthService, oauth_scheme, AuthHelper, CheckRole
from app.schemas import Tokens, GetMe


auth_router = APIRouter(prefix='/auth', tags=['Аутентификация'])


@auth_router.post("/login", summary="Получить токен по логину и паролю")
async def login(
        request: Request,
        username: str = Form(description="логин"),
        password: str = Form(description="пароль"),
        auth_service: AuthService = Depends(AuthService)
) -> Tokens:
    return await auth_service.validate_employee(username, password, request.client.host)


@auth_router.post("/refresh", response_model_exclude_none=True, summary="Обновить access токен")
async def refresh_access_token(
        refresh_token: str = Depends(oauth_scheme),
        auth_service: AuthService = Depends(AuthService)
) -> Tokens:
    return await auth_service.refresh_token(refresh_token)


@auth_router.get("/getme", summary="Получить информацию о себе")
async def get_employee_info(
        access_payload: dict = Depends(AuthHelper.authorize),
        auth_service: AuthService = Depends(AuthService)
) -> GetMe:
    return await auth_service.get_employee_info(access_payload)


@auth_router.patch("/change-shop", status_code=204, summary="Сменить магазин")
async def change_shop(
        shop_id: int,
        access_payload: dict = Depends(CheckRole([Roles.admin["id"], Roles.director["id"]])),
        auth_service: AuthService = Depends(AuthService)):
    return await auth_service.change_shop(access_payload["employee_id"], shop_id)
