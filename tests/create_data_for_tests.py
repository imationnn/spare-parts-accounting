from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

import app.models as am
from tests import data_for_test as dft
from app.services import AuthHelper


INSERT_DATA = {
    am.Brand: dft.brands,
    am.Shop: dft.shops,
    # am.Supplier: dft.suppliers,
    am.CatalogPart: dft.catalog_parts,
    am.Employee: dft.employees,
    # am.NewArrival: dft.new_arrivals,
    # am.NewArrivalDetail: dft.new_arr_detail
}


async def insert_test_data(session: AsyncSession):
    for model, data in INSERT_DATA.items():
        for item in data:
            if model.__name__ == "Employee":
                item = item.copy()
                item["password"] = AuthHelper.get_hash_password(item["password"])
            stmt = insert(model).values(item)
            await session.execute(stmt)
        await session.commit()
