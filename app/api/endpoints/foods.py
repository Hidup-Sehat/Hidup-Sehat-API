from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.default_schemas import DefaultResponse
from app.schemas.food import (
    SingleFood,
    GetAllFood,
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
            # "lastUpdated": request.lastUpdated,
            # "asupanKalori": request.asupanKalori,
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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Food for the date is already exist, please use PUT",
            )
        
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

@router.put("/user/{user_uid}/food", status_code=status.HTTP_200_OK)
async def update_food(
    user_uid: str,
    request: PostFood
):
    try:
        data = {
            # "id": request.id,
            "date": request.date,
            # "asupanKalori": request.asupanKalori,
            "totalKarbohidrat": request.totalKarbohidrat,
            "totalLemak": request.totalLemak,
            "totalSerat": request.totalSerat,
            "totalProtein": request.totalProtein,
            "makanan": [
                get_food.dict() for get_food in request.makanan
            ]
        }
        doc_ref = db.collection('users').document(user_uid).collection('food').where('date', '==', datetime.combine(request.date, datetime.min.time())).get()
        if len(list(doc_ref)) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data not found on the date",
            )
        
        doc_ref = db.collection('users').document(user_uid).collection('food').document(doc_ref[0].id)
        
        data["id"] = doc_ref.id
        data["date"] = datetime.combine(request.date, datetime.min.time())
        data["lastUpdated"] = datetime.now()
        # print(data.get('lastUpdated'))

        doc_ref.update(data)
        return DefaultResponse(
            message="Food updated successfully",
            data=data
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.get("/user/{user_uid}/food", response_model=GetAllFood, status_code=status.HTTP_200_OK)
async def get_food(
    user_uid: str,
):
    try:
        doc_ref = db.collection('users').document(user_uid).collection('food').get()
        data = []
        for doc in doc_ref:
            data.append(doc.to_dict())
        
        # print(data)
        return GetAllFood(
            food=data
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )