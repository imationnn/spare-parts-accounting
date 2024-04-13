import pytest
from httpx import AsyncClient


async def test_get_part_by_id(client: AsyncClient):
    response = await client.get("/catalog/by-id?part_id=1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["number"] == "037905237AV"
    assert response.json()["brand"] == {"id": 1, "brand_name": "Vag"}
    assert response.json()["desc_eng"] == "Distributor"
    assert response.json()["desc_rus"] == "Распределитель"
    assert response.json()["margin"] == {"id": 1, "margin_value": "1.40"}

    response = await client.get("/catalog/by-id?part_id=100")
    assert response.status_code == 404


@pytest.mark.parametrize("number, status_code, len_resp", [
    ("3556547657", 200, 2),
    ("43563423545553", 200, 0)
])
async def test_get_part_by_number(client: AsyncClient, number: str, status_code: int, len_resp: int):
    response = await client.get("/catalog/by-number?number=23552-43255")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 7
    assert response.json()[0]["number"] == "23552-43255"
    assert response.json()[0]["brand"] == {"id": 3, "brand_name": "Toyota"}
    assert response.json()[0]["desc_eng"] == "Front brake pads"
    assert response.json()[0]["desc_rus"] == "Передние тормозные колодки"

    response = await client.get(f"/catalog/by-number?number={number}")
    assert response.status_code == status_code
    assert len(response.json()) == len_resp


@pytest.mark.parametrize("new_part, status_code, result", [
    ({
         "number": "32565-54632",
         "brand_id": 1,
         "desc_eng": "Brake pads",
         "desc_rus": "Тормозные колодки",
         "margin_id": 1,
     },
     201,
     {
         "number": "32565-54632",
         "desc_eng": "Brake pads",
         "desc_rus": "Тормозные колодки",
         "id": 17,
         "brand_id": 1,
         "margin_id": 1,
         "comment": None
     }
    ),
    ({
         "number": "32565-54632",
         "brand_id": 2,
         "desc_eng": "Oil filter",
         "desc_rus": "Масляный фильтр",
         "margin_id": 2,
         "comment": "comment"
     },
     201,
     {
         "number": "32565-54632",
         "desc_eng": "Oil filter",
         "desc_rus": "Масляный фильтр",
         "id": 18,
         "brand_id": 2,
         "margin_id": 2,
         "comment": "comment"
     }),
    ({
         "number": "547732",
         "brand_id": 2,
         "desc_rus": "Масляный фильтр",
     },
     201,
     {
         "number": "547732",
         "desc_eng": None,
         "desc_rus": "Масляный фильтр",
         "id": 19,
         "brand_id": 2,
         "margin_id": 1,
         "comment": None
     }),
    ({
         "number": "547732",
         "brand_id": 2,
         "desc_rus": "Масляный фильтр",
     },
     400,
     {"detail": "Invalid parameters or existing part number passed"})
])
async def test_add_part(client: AsyncClient, new_part: dict, status_code: int, result: dict):
    response = await client.post("/catalog/new", json=new_part)
    assert response.status_code == status_code
    assert response.json() == result

    new_part = {"number": "54623", "brand_id": 2}
    response = await client.post("/catalog/new", json=new_part)
    assert response.status_code == 422

    new_part = {}
    response = await client.post("/catalog/new", json=new_part)
    assert response.status_code == 422


@pytest.mark.parametrize("part_id, edit_part, status_code, result", [
    (2,
     {
         "number": "157907437",
         "brand_id": 2,
         "desc_eng": "Brake pads",
         "desc_rus": "Тормозные колодки",
     },
     200,
     {
         "number": "157907437",
         "desc_eng": "Brake pads",
         "desc_rus": "Тормозные колодки",
         "id": 2,
         "brand_id": 2,
         "margin_id": 1,
         "comment": None
     }
     ),
    (3,
     {
         "comment": "comment"
     },
     200,
     {
         "number": "543768422C",
         "desc_eng": "Oil filter",
         "desc_rus": "Фильтр масляный",
         "id": 3,
         "brand_id": 1,
         "margin_id": 1,
         "comment": "comment"
     }
     ),
    (30,
     {"number": "157907437",
      "desc_eng": "Brake pads",
      },
     400,
     {"detail": "Invalid parameters or existing part number passed"}
     ),
    (3,
     {},
     400,
     {"detail": "Invalid parameters or existing part number passed"}
     ),
    (3,
     {"number": "4241251",
      "brand_id": 2
      },
     400,
     {"detail": "Invalid parameters or existing part number passed"}
     )
])
async def test_edit_part(client: AsyncClient, part_id: int, edit_part: dict, status_code: int, result: dict):
    response = await client.put(f"/catalog/{part_id}/edit", json=edit_part)
    assert response.status_code == status_code
    assert response.json() == result
