from starlette.testclient import TestClient

from .app.core.config import settings

prefix = f"{settings.API_PATH}/user"

user_uid = "test_user_uid"

def test_get_no_user(client: TestClient):
    resp = client.get(f"{prefix}/{user_uid}")
    assert resp.status_code == 404
    assert resp.json() == {"message": "There are no user"} 

# Example
# def test_get_categories(client: TestClient, create_category):
#     category = create_category()

#     resp = client.get(f"{prefix}/category")
#     assert resp.status_code == 200
#     data = resp.json().get("data")
#     assert data[0]["id"] == str(category.id)

# def test_get_empty_best_seller(client: TestClient):
#     resp = client.get(f"{prefix}/best-seller")
#     assert resp.status_code == 404
#     assert resp.json() == {"message": "There are no best seller items"}