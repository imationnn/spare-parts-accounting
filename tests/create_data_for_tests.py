from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

import app.models as am
from tests import data_for_test as dft


INSERT_DATA = {
    am.Brand: dft.brands,
    am.Shop: dft.shops,
    am.Supplier: dft.suppliers,
    am.CatalogPart: dft.catalog_parts,
    am.Employee: dft.employees,
    am.NewArrival: dft.new_arrivals,
    am.NewArrivalDetail: dft.new_arr_detail
}


async def insert_test_data(session: AsyncSession):
    for model, data in INSERT_DATA.items():
        for item in data:
            stmt = insert(model).values(item)
            await session.execute(stmt)
        await session.commit()
