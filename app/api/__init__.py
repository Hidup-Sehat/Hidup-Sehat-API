from fastapi import APIRouter, FastAPI
from .endpoints import emotions
from app.core.config import settings

# from app.api import utils

api_router = APIRouter()

def create_app():
    app = FastAPI()
    app.include_router(
        emotions.router,
        prefix=f"{settings.API_PATH}",
        tags=["Emotions (Natura)"])
    return app
