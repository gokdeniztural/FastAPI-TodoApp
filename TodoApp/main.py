from fastapi import FastAPI, Request
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="TodoApp/templates") # templates klasörünü tanımlandı

app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static") # static klasörünü tanımlandı

@app.get("/")
def test(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")

@app.get("/healthy")
def health_check():
    return {'status': 'healthy'}

app.include_router(auth.router) # auth.py dosyasındaki router'ı main'e dahil ettiğimiz kısım.
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)