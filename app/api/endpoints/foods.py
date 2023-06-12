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

@router.post("/users/{userId}/food", status_code=status.HTTP_201_CREATED)
async def create_food(
    userId: str,
    request: PostFood
):
    try:
        data = {
            "date": request.date,
            "lastUpdated": request.lastUpdated,
            # "asupanKalori": request.asupanKalori,
            "totalKarbohidrat": request.totalKarbohidrat,
            "totalLemak": request.totalLemak,
            "totalSerat": request.totalSerat,
            "totalProtein": request.totalProtein,
            "makanan": [
                get_food.dict() for get_food in request.makanan
            ]
        }
        
        doc_ref = db.collection('users').document(userId).collection('food').document()

        data["id"] = doc_ref.id
        data["date"] = datetime.combine(date.today(), datetime.min.time())
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

@router.put("/user/{userId}/food", status_code=status.HTTP_200_OK)
async def update_food(
    userId: str,
    request: PostFood
):
    try:
        data = {
            "id": request.id,
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
        doc_ref = db.collection('users').document(userId).collection('food').where('date', '==', datetime.combine(date.today(), datetime.min.time())).get()
        if len(list(doc_ref)) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data not found on the date",
            )
        
        doc_ref = db.collection('users').document(userId).collection('food').document(doc_ref[0].id)
        
        data["date"] = datetime.combine(date.today(), datetime.min.time())
        data["lastUpdated"] = datetime.now()

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

@router.get("/user/{userId}/food", response_model=GetAllFood, status_code=status.HTTP_200_OK)
async def get_food(
    userId: str
):
    try:
        doc_ref = db.collection('users').document(userId).collection('food').where('date', '==', datetime.combine(date.today(), datetime.min.time())).get()
        data = []
        for doc in doc_ref:
            data.append(doc.to_dict())
        return GetAllFood(
            food=data
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )