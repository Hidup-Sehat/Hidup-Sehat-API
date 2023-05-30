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

# @router.get("/testing/{user_id}", status_code=status.HTTP_200_OK)
# async def get_user(user_id: str):
#     docs = db.collection('user').document(user_id).get()
#     print(docs.to_dict())
#     if docs.exists:
#         return docs.to_dict()
#     else:
#         return None

@router.get("/user/{user_id}/", response_model=GetUserDetail, status_code=status.HTTP_200_OK)
async def get_user_detail(
    user_id: str,
):
    try:
        user = db.collection('users').document(user_id).get()

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