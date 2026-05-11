from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos, admin


app = FastAPI()

models.Base.metadata.create_all(bind=engine) # Bu satır sadece todos.db mevcut değilse çalışacaktır! / Tablo oluşturuldu

app.include_router(auth.router) # auth.py dosyasındaki router'ı main'e dahil ettiğimiz kısım.
app.include_router(todos.router)
app.include_router(admin.router)