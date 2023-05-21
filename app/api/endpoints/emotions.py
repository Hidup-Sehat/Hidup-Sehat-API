from fastapi import APIRouter, status
from app.schemas.emotion import (
    GetUserEmotion,
    CreateUserEmotion
)

router = APIRouter()

@router.get("/emotions", response_model=GetUserEmotion, status_code=status.HTTP_200_OK)
async def get_emotions():
    return {"message": "This is the emotion endpoint"}

@router.post("/emotions", response_model=CreateUserEmotion, status_code=status.HTTP_200_OK)
async def create_emotions():
    return {"message": "This is the emotion endpoint"}