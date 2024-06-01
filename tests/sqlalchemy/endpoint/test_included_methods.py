import pytest
from fastapi.testclient import TestClient

from CRUDFastAPI import CRUDFastAPI, crud_router

from ...sqlalchemy.conftest import get_session_local


@pytest.mark.asyncio
async def test_included_methods(client: TestClient, async_session, test_model, create_schema, update_schema):
    custom_router = crud_router(
        session=get_session_local,
        model=test_model,
        crud=CRUDFastAPI(test_model),
        create_schema=create_schema,
        update_schema=update_schema,
        included_methods=["create", "read"],
        path="/test_custom",
        tags=["Test"],
    )

    client.app.include_router(custom_router)

    response = client.post("/test_custom/create", json={"name": "Test Item", "tier_id": 1})
    assert response.status_code == 200

    item_id = response.json()["id"]
    response = client.get(f"/test_custom/get/{item_id}")
    assert response.status_code == 200

    response = client.patch(f"/test_custom/update/{item_id}", json={"name": "Updated"})
    assert response.status_code == 404


def test_endpoint_creation_conflict(endpoint_creator):
    with pytest.raises(ValueError) as exc_info:
        endpoint_creator.add_routes_to_router(included_methods=["create", "read"], deleted_methods=["update", "delete"])
    assert "Cannot use both 'included_methods' and 'deleted_methods' simultaneously" in str(exc_info.value)


def test_invalid_included_methods(endpoint_creator):
    with pytest.raises(ValueError) as exc_info:
        endpoint_creator.add_routes_to_router(included_methods=["fly", "dig"])
    assert "Invalid CRUD methods in included_methods" in str(exc_info.value)
