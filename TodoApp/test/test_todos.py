from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..routers.todos import get_db, get_current_user
from ..database import Base 
from ..main import app
from ..models import Todos

from fastapi import status
from fastapi.testclient import TestClient

import pytest


SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db" # test için sqlite kullanabiliriz. Production için
                                                  # postgresql kullanımımız devam ediyor.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass = StaticPool 
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine) # test veritabanında tabloları oluşturmak için kullanıyoruz.

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'testuser', 'id': 1, 'user_role': 'admin'}

app.dependency_overrides[get_db] = override_get_db
# uygulama çalışırken get_db bağımlılığı istenilen yerlerde bu fonksiyonun çalışmasını sağlıyoruz. 
# böylece test veritabanını kullanarak testlerimizi yapıyoruz !!!

app.dependency_overrides[get_current_user] = override_get_current_user
# uygulama çalışırken get_current_user bağımlılığı istenilen yerlerde bu fonksiyon kullanılır. JWT yok!!


client = TestClient(app) 

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn the code!",
        description = "Need to learn everyday!",
        priority = 5,
        complete = False,
        owner_id = 1 # test_user id'sini 1 yapmıştık !
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos")) # test tamamlandıktan sonra test.db tablolarını temizler!
        connection.commit()


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

