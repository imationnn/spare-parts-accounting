from fastapi import HTTPException, Depends
from sqlalchemy.exc import StatementError

from app.repositories import SupplierRepository, OrganizationAttrRepository
from app.schemas import SupplierOut, SupplierIn, SupplierListOut, SupplierUpdate


class SupplierService:

    def __init__(
            self,
            repository: SupplierRepository = Depends(),
            org_attr_repository: OrganizationAttrRepository = Depends()
    ):
        self.repository = repository
        self.org_attr_repository = org_attr_repository

    async def _get_supplier_by_id(self, supplier_id: int) -> SupplierRepository.model:
        result = await self.repository.get_supplier(supplier_id)
        if not result:
            raise HTTPException(404)
        return result

    async def get_supplier_by_id(self, supplier_id: int) -> SupplierOut:
        supplier_model = await self._get_supplier_by_id(supplier_id)
        return SupplierOut.model_validate(supplier_model, from_attributes=True)

    async def get_all_suppliers(self, limit: int = 500, offset: int = 0) -> list[SupplierListOut]:
        result = await self.repository.get_multi(limit=limit, offset=offset)
        return [SupplierListOut.model_validate(item, from_attributes=True) for item in result]

    async def add_new_supplier(self, supplier: SupplierIn) -> SupplierOut:
        attr_model = await self.org_attr_repository.add_organization_attrs(
            **supplier.org_attr.model_dump(exclude_none=True)
        )
        sup_model = await self.repository.add_new_supplier(
            org_name=supplier.org_name,
            org_attr_id=attr_model.id
        )
        sup_model.org_attr = attr_model
        await self.repository.session.commit()
        return SupplierOut.model_validate(sup_model, from_attributes=True)

    async def update_supplier(self, supplier_id: int, supplier_upd: SupplierUpdate) -> SupplierOut:
        supplier = await self._get_supplier_by_id(supplier_id)
        try:
            updated_supplier = await self.repository.update_supplier(
                supplier,
                supplier_upd.model_dump(exclude_unset=True)
            )
        except StatementError:
            raise HTTPException(400)
        return SupplierOut.model_validate(updated_supplier, from_attributes=True)
