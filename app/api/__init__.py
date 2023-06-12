from fastapi import APIRouter, FastAPI
from .endpoints import users, homes, activity, feeds, emotion, foods, faqs
from app.core.config import settings
from app.deps.firebase import db
from app.deps.encrypt import generate_key

# from app.api import utils

api_router = APIRouter()

def create_app():
    app = FastAPI()

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
    app.include_router(
        faqs.router,
        prefix=f"{settings.API_PATH}",
        tags=["FAQs"]
    )
    
    # Example of using firebase
    @app.get("/test/{user_id}")
    async def get_user(user_id: str):
        doc_ref = db.collection('user').document(user_id)
        doc = doc_ref.get()
        print(doc.to_dict())
        if doc.exists:
            return doc.to_dict()
        else:
            return None
    return app
