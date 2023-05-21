from fastapi import APIRouter, FastAPI
from .endpoints import users, homes
from app.core.config import settings

# from app.api import utils

api_router = APIRouter()

def create_app():
    app = FastAPI()
    app.include_router(
        homes.router,
        prefix=f"{settings.API_PATH}",
        tags=["Home (Natura)"])
    app.include_router(
        users.router,
        prefix=f"{settings.API_PATH}",
        tags=["User (Edy)"])
    return app
