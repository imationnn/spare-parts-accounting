from sqlalchemy.exc import StatementError, NoResultFound

from app.repositories import ShopRepository
from app.schemas import ShopOut, ShopIn, ShopUpd
from app.services import BaseService
from app.exceptions import ShopBadParameters, ShopNotFound


class ShopService(BaseService):
    repository = ShopRepository()

    async def get_shop_by_id(self, shop_id: int) -> ShopOut:
        result = await self.repository.get_shop(id=shop_id)
        if not result:
            raise ShopNotFound
        return ShopOut.model_validate(result, from_attributes=True)

    async def get_all_shops(self) -> list[ShopOut]:
        result = await self.repository.get_all_shops()
        return [ShopOut.model_validate(item, from_attributes=True) for item in result]

    async def add_new_shop(self, new_shop: ShopIn) -> ShopOut:
        values = new_shop.model_dump(exclude_none=True)
        try:
            result = await self.repository.add_shop(**values)
            await self.repository.session.commit()
        except StatementError:
            raise ShopBadParameters
        return ShopOut.model_validate(result, from_attributes=True)

    async def update_shop(self, shop_id: int, shop: ShopUpd) -> ShopOut:
        values = shop.model_dump(exclude_none=True)
        if not values:
            raise ShopBadParameters
        try:
            result = await self.repository.edit_shop(shop_id, **values)
            await self.repository.session.commit()
        except StatementError:
            raise ShopBadParameters
        except NoResultFound:
            raise ShopNotFound
        return ShopOut.model_validate(result, from_attributes=True)
