from fastapi import APIRouter, FastAPI
from .endpoints import users, homes, activity, feeds, emotion, foods
from app.core.config import settings
from app.deps.firebase import db
from app.deps.encrypt import generate_key

api_router = APIRouter()

def create_app():
    app = FastAPI()

    # GENERATE KEY for encryption & decryption
    # generate_key()

    app.include_router(
        homes.router,
        prefix=f"{settings.API_PATH}",
        tags=["Home"])
    app.include_router(
        users.router,
        prefix=f"{settings.API_PATH}",
        tags=["User"])
    app.include_router(
        activity.router,
        prefix=f"{settings.API_PATH}",
        tags=["Activity"])
    app.include_router(
        feeds.router,
        prefix=f"{settings.API_PATH}",
        tags=["Feeds"])
    app.include_router(
        emotion.router,
        prefix=f"{settings.API_PATH}",
        tags=["Emotion"])
    app.include_router(
        foods.router,
        prefix=f"{settings.API_PATH}",
        tags=["Foods"])

    return app
