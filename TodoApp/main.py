<<<<<<< HEAD
=======
import utils.http_session
>>>>>>> a07f8082b35bcb6d2f7a6fc00babc4ce9206809d
from fastapi import FastAPI
from .routers import auth, todos, admin, users
from .models import Base
from .database import engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def health_check():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

