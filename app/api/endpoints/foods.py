from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.default_schemas import DefaultResponse
from app.schemas.food import (
    SingleFood,
    GetFoodByDate,
    PostFood    
)
from datetime import date, datetime
from app.deps.firebase import db

router = APIRouter()

@router.post("/users/{user_uid}/food", status_code=status.HTTP_201_CREATED)
async def create_food(
    user_uid: str,
    request: PostFood
):
    try:
        data = {
            "date": request.date,
            "totalKarbohidrat": request.totalKarbohidrat,
            "totalLemak": request.totalLemak,
            "totalSerat": request.totalSerat,
            "totalProtein": request.totalProtein,
            "makanan": [
                get_food.dict() for get_food in request.makanan
            ]
        }
        
        dateExist = db.collection('users').document(user_uid).collection('food').where('date', '==', datetime.combine(request.date, datetime.min.time())).get()
        if len(dateExist) > 0:
            doc_ref = db.collection('users').document(user_uid).collection('food').document(dateExist[0].id)
            doc = doc_ref.get().to_dict()

            data["makanan"] = doc["makanan"] + data["makanan"]
        else:
            doc_ref = db.collection('users').document(user_uid).collection('food').document()

        data["id"] = doc_ref.id
        data["date"] = datetime.combine(request.date, datetime.min.time())
        data["lastUpdated"] = datetime.now()


        doc_ref.set(data)
        return DefaultResponse(
            message="Food created successfully",
            data=data
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.get("/user/{user_uid}/food/{date}", response_model=GetFoodByDate, status_code=status.HTTP_200_OK)
async def get_food(
    user_uid: str,
    date: date
):
    try:
        doc_ref = db.collection('users').document(user_uid).collection('food').where('date', '==', datetime.combine(date, datetime.min.time())).get()

        if len(list(doc_ref)) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data not found on the date",
            )
        data = doc_ref[0].to_dict()

        return GetFoodByDate(
            food=data
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )