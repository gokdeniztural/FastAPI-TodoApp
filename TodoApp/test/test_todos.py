from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..routers.todos import get_db, get_current_user
from ..database import Base 
from ..main import app

from fastapi import status
from fastapi.testclient import TestClient

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

def test_read_all_authenticated():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK # 200 durum kodu dönmeli
    assert response.json() == [] # Burada şuan testdb.db boş olduğu için boş liste dönmeli. İleride değişecek!!

