from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users


app = FastAPI()

Base.metadata.create_all(bind=engine) # Bu satır sadece todos.db mevcut değilse çalışacaktır! / Tablo oluşturuldu

@app.get("/healthy")
def health_check():
    return {'status': 'healthy'}

app.include_router(auth.router) # auth.py dosyasındaki router'ı main'e dahil ettiğimiz kısım.
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)