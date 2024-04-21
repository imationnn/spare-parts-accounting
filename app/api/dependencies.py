from fastapi import Depends

from app.models import Roles
from app.services import AuthHelper, CheckRole


token_dep = Depends(AuthHelper.authorize)
check_role_dep = Depends(CheckRole([Roles.admin["id"], Roles.director["id"]]))
