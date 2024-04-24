from app.repositories import BaseRepository
from app.models import OrgAttr


class OrganizationAttrRepository(BaseRepository):
    model = OrgAttr

    async def add_organization_attrs(self, **values):
        return await self.add_one(**values)
