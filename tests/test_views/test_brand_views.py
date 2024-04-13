import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("brand_name, status_code, len_resp, result", [
    ("Vag", 200, 1, {'id': 1}),
    ("example", 404, 1, {"detail": "Brand not found"})
]
                         )
async def test_get_brand_by_name(client: AsyncClient, brand_name: str, status_code: int, len_resp: int, result: dict):
    response = await client.get(f"/brands/by-name?brand_name={brand_name}")
    assert response.status_code == status_code
    assert len(response.json()) == len_resp
    assert response.json() == result


@pytest.mark.parametrize("brand_id, status_code, len_resp, result", [
    (1, 200, 1, {'brand_name': 'Vag'}),
    (21231324, 404, 1, {"detail": "Brand not found"})
]
                         )
async def test_get_brand_by_id(client: AsyncClient, brand_id: int, status_code: int, len_resp: int, result: dict):
    response = await client.get(f"/brands/by-id?brand_id={brand_id}")
    assert response.status_code == status_code
    assert len(response.json()) == len_resp
    assert response.json() == result


@pytest.mark.parametrize("new_brand, status_code, len_resp, result", [
    ({"brand_name": "ATE"}, 201, 2, {"id": 7, "brand_name": "ATE"}),
    ({"brand_name": "ATE"}, 409, 1, {"detail": "Brand already exist"})
]
                         )
async def test_add_new_brand(client: AsyncClient, new_brand: dict, status_code: int, len_resp: int, result: dict):
    response = await client.post("/brands/new", json=new_brand)
    assert response.status_code == status_code
    assert len(response.json()) == len_resp
    assert response.json() == result


@pytest.mark.parametrize("edit_brand, status_code, len_resp, result", [
    ({"id": 1, "brand_name": "VAG"}, 200, 2, {"id": 1, "brand_name": "VAG"}),
    ({"id": 1, "brand_name": "Vag"}, 200, 2, {"id": 1, "brand_name": "Vag"}),
    ({"id": 2, "brand_name": "Vag"}, 409, 1, {"detail": "Brand already exist"}),
    ({"id": 100, "brand_name": "VAG"}, 404, 1, {"detail": "Brand not found"})
]
                         )
async def test_edit_brand(client: AsyncClient, edit_brand: dict, status_code: int, len_resp: int, result: dict):
    response = await client.patch("/brands/edit", json=edit_brand)
    assert response.status_code == status_code
    assert len(response.json()) == len_resp
    assert response.json() == result
