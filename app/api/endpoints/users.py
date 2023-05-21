from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.user import (
    CreateUserDetail,
)

router = APIRouter()

@router.post("/user-detail", status_code=status.HTTP_200_OK)
async def create_user_detail(
    request: CreateUserDetail
) -> JSONResponse:
    return {"message": "This is the user detail post endpoint"}