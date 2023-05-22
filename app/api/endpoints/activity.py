from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.activity import (
    GetAllActivity,
    GetActivityMovement
)

router = APIRouter()

@router.get("/activity", response_model=GetAllActivity, status_code=status.HTTP_200_OK)
async def get_all_activity():
    return {"id": "123", "cardColor": 1, "type": "string", "category": "string", "difficulty": "string", "imgUrl": "string", "movementCount": 1}

@router.get("/activity/{activity_id}", response_model=GetActivityMovement, status_code=status.HTTP_200_OK)
async def get_activity_movement(activity_id: str):
    return {"id": "123", "movementData": [
        {
            "sudutSikuKanan": 1,
            "sudutSikuKiri": 1,
            "sudutKetiakKanan": 1,
            "sudutKetiakKiri": 1,
            "sudutPundakKanan": 1,
            "sudutPundakKiri": 1,
            "sudutPinggulKanan": 1,
            "sudutPinggulKiri": 1,
            "sudutPahaKanan": 1,
            "sudutPahaKiri": 1,
            "sudutLututKanan": 1,
            "sudutLututKiri": 1
        }]
    }