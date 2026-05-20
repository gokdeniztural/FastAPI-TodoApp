from .utils import *
from ..routers.admin import get_db, get_current_user
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
    "priority": 5,
    "description": "Need to learn everyday!",
    "id": 1,
    "complete": False,
    "title": "Learn the code!",
    "owner_id": 1
}]