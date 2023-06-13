from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.home import (
    GetUserDetail,
    UpdateUserStatisticTarget,
    CreateUserEmotion
)
from datetime import datetime
from app.deps.firebase import db

router = APIRouter()

@router.get("/user/{user_uid}/", response_model=GetUserDetail, status_code=status.HTTP_200_OK)
async def get_user_detail(
    user_uid: str,
):
    try:
        user = db.collection('users').document(user_uid).get()

        if not user.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        userDetail = user.to_dict()

        userDetail['registeredAt'] = datetime.fromtimestamp(userDetail['registeredAt'].timestamp())

        return GetUserDetail(**userDetail)


    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
