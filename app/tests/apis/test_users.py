from starlette.testclient import TestClient

from .app.core.config import settings

prefix = f"{settings.API_PATH}/user"

user_uid = "test_user_uid"

def test_get_no_user(client: TestClient):
    resp = client.get(f"{prefix}/{user_uid}")
    assert resp.status_code == 404
    assert resp.json() == {"message": "There are no user"} 