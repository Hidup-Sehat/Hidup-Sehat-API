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

@router.post("/user/{user_uid}/revert-statistics", status_code=status.HTTP_200_OK)
async def revert_user_statistic_target(
    user_uid: str
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
            gender = doc_snapshot.get('gender')
            age = doc_snapshot.get('age')
            height = doc_snapshot.get('height')
            weight = doc_snapshot.get('weight')
            
            if gender.lower() == "male":
                bmr = 66 + (13.75 * weight) + (5 * height) - (6.75 * age)
            elif gender.lower() == "female":
                bmr = 655 + (9.56 * weight) + (1.85 * height) - (4.68 * age)

            calorieNeeds = int(bmr * 1.2)
            waterNeeds = weight * 0.033

            doc_ref.update({
                'calorieNeeds': calorieNeeds,
                'waterNeeds': waterNeeds
            })

            return {
                'message': 'Revert user statistic target success',
                'data': {
                    'calorieNeeds': calorieNeeds,
                    'waterNeeds': waterNeeds
                }
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