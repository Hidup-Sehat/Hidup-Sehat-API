from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.home import (
    GetUserStatistic,
    UpdateUserStatisticTarget,
    CreateUserEmotion
)

router = APIRouter()

@router.get("/user-statistic", response_model=GetUserStatistic, status_code=status.HTTP_200_OK)
async def get_user_statistic():
    return {"message": "This is the User Statistic endpoint"}

@router.put("/user-statistic-target", status_code=status.HTTP_200_OK)
async def update_user_statistic_target(
    request: UpdateUserStatisticTarget
) -> JSONResponse:
    return {"message": "This is the user statistic target put endpoint"}


@router.post("/emotion", status_code=status.HTTP_201_CREATED)
async def create_emotion(
    request: CreateUserEmotion
) -> JSONResponse:
    if request.CreateUserEmotion.emotion == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Emotion is empty",
        )
    return {"message": "This is the emotion post endpoint"}