from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.repositories import BaseRepository
from app.models import Supplier


class SupplierRepository(BaseRepository):
    model = Supplier

    async def get_supplier(self, supplier_id: int) -> model:
        stmt = select(self.model).options(joinedload(self.model.org_attr)).where(self.model.id == supplier_id)
        result = await self.session.scalars(stmt)
        return result.one_or_none()

    async def add_new_supplier(self, org_name: str, org_attr_id: int) -> model:
        return await self.add_one(org_name=org_name, org_attr_id=org_attr_id)

    async def update_supplier(self, supplier_model: Supplier, supplier_data: dict) -> model:
        for supplier_key, supplier_value in supplier_data.items():
            if not isinstance(supplier_value, dict):
                setattr(supplier_model, supplier_key, supplier_value)
                continue
            for org_attr_key, org_attr_value in supplier_value.items():
                setattr(supplier_model.org_attr, org_attr_key, org_attr_value)
        self.session.add(supplier_model)
        await self.session.commit()
        return supplier_model
