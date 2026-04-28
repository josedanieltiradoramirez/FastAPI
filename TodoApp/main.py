from fastapi import FastAPI, Request, status

from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
try:
    from .routers import auth, todos
except ImportError:
    from routers import auth, todos
try:
    from . import models
    from .models import Todos
    from .database import engine, SessionLocal, ensure_sqlite_column
except ImportError:
    import models
    from models import Todos
    from database import engine, SessionLocal, ensure_sqlite_column
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse


app = FastAPI()


app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")

@app.get("/")
def test(request: Request):
    return RedirectResponse(url='/todos/todo-page', status_code=status.HTTP_302_FOUND)

@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}

Base.metadata.create_all(bind = engine)
ensure_sqlite_column(engine, "todos", "owner_id", "INTEGER")

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
