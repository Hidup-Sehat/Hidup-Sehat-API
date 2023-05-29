from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.default_schemas import DefaultResponse
from app.schemas.activity import (
    CreateActivity,
    GetAllActivity,
    GetActivityMovement,
)
from app.deps.firebase import db

router = APIRouter()

@router.post("/activity", status_code=status.HTTP_201_CREATED)
async def create_activity(
    request: CreateActivity
):
    try: 
        data = {
            "id": request.id,
            "cardColor": request.cardColor,
            "type": request.type,
            "category": request.category,
            "difficulty": request.difficulty,
            "imgUrl": request.imgUrl,
            "movementCount": request.movementCount,
            "movementList": [get_movement_list.dict() for get_movement_list in request.movementList]
        }
        doc_ref = db.collection('activities').document()

        data["id"] = doc_ref.id
        doc_ref.set(data)
        return DefaultResponse(
            message="Activity created successfully",
            data=data
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
@router.post("/activity/{activity_id}/movement", status_code=status.HTTP_201_CREATED)
async def create_activity_movement(
    activity_id: str, 
    request: GetActivityMovement
):
    try:
        data = {
            "id": request.id,
            "sudutSikuKanan": request.sudutSikuKanan,
            "sudutSikuKiri": request.sudutSikuKiri,
            "sudutKetiakKanan": request.sudutKetiakKanan,
            "sudutKetiakKiri": request.sudutKetiakKiri,
            "sudutPundakKanan": request.sudutPundakKanan,
            "sudutPundakKiri": request.sudutPundakKiri,
            "sudutPinggulKanan": request.sudutPinggulKanan,
            "sudutPinggulKiri": request.sudutPinggulKiri,
            "sudutPahaKanan": request.sudutPahaKanan,
            "sudutPahaKiri": request.sudutPahaKiri,
            "sudutLututKanan": request.sudutLututKanan,
            "sudutLututKiri": request.sudutLututKiri,
        }

        doc_ref = db.collection('activities').document(activity_id).collection('movementList').document()

        data["id"] = 0
        doc_data = db.collection('activities').document(activity_id).collection('movementList').get()
        if doc_data:
            data["id"] += len(doc_data)

        doc_ref.set(data)

        return DefaultResponse(
            message="Activity movement created successfully",
            data=data
        )
    
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
@router.get("/activity", response_model=GetAllActivity, status_code=status.HTTP_200_OK)
async def get_all_activity():
    try:
        activity = db.collection('activities')
        docs = activity.stream()

        activity = []  

        for doc in docs:
            doc_data = doc.to_dict()
            activity.append(doc_data)

        return GetAllActivity(activity=activity)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

#! This endpoint is still in bug
@router.get("/activity/{activity_id}/movement/{index}", response_model=GetActivityMovement, status_code=status.HTTP_200_OK)
async def get_activity_movement(
    activity_id: str,
    index: int
):
    try: 
        doc_ref = db.collection('activities').document(activity_id).collection('movementList').where('id', '==', index).get()

        for doc in doc_ref:
            doc_data = doc.to_dict()

        if doc_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movement activity not found",
            )
        
        data = {
            "id": doc_data["id"],
            "sudutSikuKanan": doc_data["sudutSikuKanan"],
            "sudutSikuKiri": doc_data["sudutSikuKiri"],
            "sudutKetiakKanan": doc_data["sudutKetiakKanan"],
            "sudutKetiakKiri": doc_data["sudutKetiakKiri"],
            "sudutPundakKanan": doc_data["sudutPundakKanan"],
            "sudutPundakKiri": doc_data["sudutPundakKiri"],
            "sudutPinggulKanan": doc_data["sudutPinggulKanan"],
            "sudutPinggulKiri": doc_data["sudutPinggulKiri"],
            "sudutPahaKanan": doc_data["sudutPahaKanan"],
            "sudutPahaKiri": doc_data["sudutPahaKiri"],
            "sudutLututKanan": doc_data["sudutLututKanan"],
            "sudutLututKiri": doc_data["sudutLututKiri"],
        }
        
        return GetActivityMovement(**data)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
