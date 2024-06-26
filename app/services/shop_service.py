from fastapi import Depends
from sqlalchemy.exc import StatementError, NoResultFound

from app.repositories import ShopRepository
from app.schemas import ShopOut, ShopIn, ShopUpd, ShopDelete
from app.exceptions import ShopBadParameters, ShopNotFound, ShopCannotBaDeleted


class ShopService:

    def __init__(self, repository: ShopRepository = Depends()):
        self.repository = repository

    async def get_shop_by_id(self, shop_id: int) -> ShopOut:
        result = await self.repository.get_shop(id=shop_id)
        if not result:
            raise ShopNotFound
        return ShopOut.model_validate(result)

    async def get_all_shops(self) -> list[ShopOut]:
        result = await self.repository.get_all_shops()
        return [ShopOut.model_validate(item) for item in result]

    async def add_new_shop(self, new_shop: ShopIn) -> ShopOut:
        values = new_shop.model_dump(exclude_none=True)
        try:
            result = await self.repository.add_shop(**values)
            await self.repository.session.commit()
        except StatementError:
            raise ShopBadParameters
        return ShopOut.model_validate(result)

    async def update_shop(self, shop_id: int, shop: ShopUpd) -> ShopOut:
        values = shop.model_dump(exclude_unset=True)
        if not values:
            raise ShopBadParameters
        try:
            result = await self.repository.edit_shop(shop_id, **values)
            await self.repository.session.commit()
        except StatementError:
            raise ShopBadParameters
        except NoResultFound:
            raise ShopNotFound
        return ShopOut.model_validate(result)

    async def delete_shop(self, shop_id: int) -> ShopDelete:
        try:
            result = await self.repository.delete_one(shop_id)
            await self.repository.session.commit()
        except StatementError:
            raise ShopCannotBaDeleted
        except NoResultFound:
            raise ShopNotFound
        return ShopDelete.model_validate(result)
