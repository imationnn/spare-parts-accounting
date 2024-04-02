from httpx import AsyncClient


async def test_get_all_margins(client: AsyncClient):
    response = await client.get("/margins/all")
    assert response.status_code == 200
    assert response.json()[0] == {'id': 1, 'margin_value': '1.40'}
    assert response.json()[1] == {'id': 2, 'margin_value': '1.50'}
    assert response.json()[2] == {'id': 3, 'margin_value': '1.60'}


async def test_edit_margin_category(client: AsyncClient):
    edit_category = {"id": 1, "margin_value": 2}
    response = await client.patch("/margins/edit", json=edit_category)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "margin_value": '2.00'}
    edit_category = {"id": 1, "margin_value": 1.4}
    response = await client.patch("/margins/edit", json=edit_category)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "margin_value": '1.40'}
