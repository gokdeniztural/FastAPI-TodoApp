from ..routers.todos import get_db, get_current_user
from fastapi import status
from .utils import *

app.dependency_overrides[get_db] = override_get_db
# uygulama çalışırken get_db bağımlılığı istenilen yerlerde bu fonksiyonun çalışmasını sağlıyoruz. 
# böylece test veritabanını kullanarak testlerimizi yapıyoruz !!!

app.dependency_overrides[get_current_user] = override_get_current_user
# uygulama çalışırken get_current_user bağımlılığı istenilen yerlerde bu fonksiyon kullanılır. JWT yok!!


def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK # 200 durum kodu dönmeli
    assert response.json() == [{
        "title": "Learn the code!",
        "description": "Need to learn everyday!",
        "id": 1,
        "priority": 5,
        "complete": False,
        "owner_id": 1
    }] # test_todo fixture'ında oluşturduğumuz todo'nun json formatında döndüğünü doğruluyoruz


def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "title": "Learn the code!",
        "description": "Need to learn everyday!",
        "id": 1,
        "priority": 5,
        "complete": False,
        "owner_id": 1
    }

def test_read_one_authenticated_not_found():
    response = client.get("/todo/999") # var olmayan bir todo id'si ile istek yapıyoruz
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo(test_todo):
    request_data = {
        "title": "New Todo",
        "description": "New todo description",
        "priority": 5,
        "complete": False,
    }
    response = client.post("/todo", json=request_data)
    assert response.status_code == 201

    # Oluşturulan todo'nun veritabanında doğru şekilde kaydedildiğini gözle görmek için yapıyoruz!
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()# test_todo fixture'ında oluşturduğumuz todo'nun id'si 1, yeni oluşturduğumuz todo'nun id'si 2 olacak
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")


def test_update_todo(test_todo):
    request_data = {
        'title': 'Change the title of the todo already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
    }
    response = client.put("/todo/1", json=request_data)
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first() 

    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")


def test_update_todo_not_found(test_todo):
    request_data = {
        'title': 'Change the title of the todo already saved!',
        'description': 'Need to learn everyday!',
        'priority': 5,
        'complete': False,
    }
    response = client.put("/todo/999", json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found'}

def test_delete_todo(test_todo):
    response = client.delete("/todo/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None # silindiği için model None olmalı

def test_delete_todo_not_found():
    response = client.delete("/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found'}

# ========== Test Senaryoları Bu Şekilde ==========
# 1. İstek at (client.get/post/put/delete)
# 2. Status code kontrol et
# 3. Gerekirse DB'ye bak veya json kontrol et