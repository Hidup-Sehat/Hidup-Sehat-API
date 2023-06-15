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

@router.put("/user/{user_uid}/statistics", status_code=status.HTTP_200_OK)
async def update_user_statistic_target(
    user_uid: str,
    request: UpdateUserStatisticTarget
):
    try:
        doc_ref = db.collection('users').document(user_uid)
        doc_snapshot = doc_ref.get()

        if not doc_snapshot.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        try:
            doc_ref.update({
                'calorieNeeds': request.calorieNeeds,
                'calorieBurnedNeeds': request.calorieBurnedNeeds,
                'sleepNeeds': request.sleepNeeds,
                'waterNeeds': request.waterNeeds
            })
            return {
                'message': 'Update user statistic target success',
                'data': request.dict()
            }
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

        # user = db.collection('users').document(user_uid).get()

        # if not user.exists:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail="User not found",
        #     )

        # userDetail = user.to_dict()

        # userDetail['calorieNeeds'] = request.CalorieNeeds
        # userDetail['calorieBurnedNeeds'] = request.CalorieBurnedNeeds
        # userDetail['sleepNeeds'] = request.SleepNeeds
        # userDetail['waterNeeds'] = request.WaterNeeds

        # db.collection('users').document(user_uid).update(userDetail)

        # return JSONResponse(
        #     status_code=status.HTTP_200_OK,
        #     content={
        #         "message": "Update user statistic target success",
        #         "data": userDetail            
        #     }
        # )

    # except ValueError as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=str(e),
    #     )
