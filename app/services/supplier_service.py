from fastapi import HTTPException, Depends

from app.repositories import SupplierRepository, OrganizationAttrRepository
from app.schemas import SupplierOut, SupplierIn


class SupplierService:

    def __init__(
            self,
            repository: SupplierRepository = Depends(),
            org_attr_repository: OrganizationAttrRepository = Depends()
    ):
        self.repository = repository
        self.org_attr_repository = org_attr_repository

    async def get_supplier_by_id(self, supplier_id: int) -> SupplierOut:
        result = await self.repository.get_supplier(supplier_id)
        if not result:
            raise HTTPException(404)
        return SupplierOut.model_validate(result, from_attributes=True)

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
