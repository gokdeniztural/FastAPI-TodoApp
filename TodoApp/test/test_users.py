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

def test_change_password_success(test_user):
    response = client.put("/user/password", json = {"password": "testpassword", 
                                                    "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/password", json = {"password": "wrongpassword", 
                                                    "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}

def test_change_phone_number_success(test_user):
    response = client.put("/user/phone_number/0533-123-12 34")
    assert response.status_code == status.HTTP_204_NO_CONTENT