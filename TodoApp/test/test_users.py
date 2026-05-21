from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    data = response.json()
    assert data["username"] == "tolgatural"
    assert data["email"] == "tolgatural@example.com"
    assert data["first_name"] == "Tolga"
    assert data["last_name"] == "Tural"
    assert data["role"] == "admin"
    assert data["phone_number"] == "0533-123-12 34"