from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..routers.todos import get_db
from ..database import Base 
from ..main import app



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



app.dependency_overrides[get_db] = override_get_db
# uygulama çalışırken get_db bağımlılığı istenilen yerlerde bu fonksiyonun çalışmasını sağlıyoruz. 
# böylece test veritabanını kullanarak testlerimizi yapıyoruz !!!
