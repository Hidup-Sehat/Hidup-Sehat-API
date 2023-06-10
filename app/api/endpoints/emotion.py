from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.default_schemas import DefaultResponse
from app.schemas.emotion import (
    Emotion,
    GetEmotion
)
from datetime import date, datetime
from app.deps.firebase import db

router = APIRouter()

@router.post("/user/{userId}/emotion", status_code=status.HTTP_201_CREATED)
async def create_emotion(
    userId: str,
    request: Emotion
):
    try: 
        data = {
            "id": request.id,
            "date": request.date,
            "lastUpdated": request.lastUpdated,
            "emotionPositive": request.emotionPositive,
            "emotionNegative": request.emotionNegative,
            "emotionSource": request.emotionSource,
            "note": request.note
        }

        dateExist = db.collection('users').document(userId).collection('emotions').where('date', '==', datetime.combine(date.today(), datetime.min.time())).get()
        if len(dateExist) > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Emotion for today already exist, please use PUT",
            )

        doc_ref = db.collection('users').document(userId).collection('emotions').document()

        data["id"] = doc_ref.id
        data["date"] = datetime.combine(date.today(), datetime.min.time())
        data["lastUpdated"] = datetime.now()
        doc_ref.set(data)
        return DefaultResponse(
            message="Emotion created successfully",
            data=data
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.put("/user/{userId}/emotion", status_code=status.HTTP_200_OK)
async def update_emotion(
    userId: str,
    request: Emotion
):
    try:
        data = {
            "id": request.id,
            "date": request.date,
            "lastUpdated": request.lastUpdated,
            "emotionPositive": request.emotionPositive,
            "emotionNegative": request.emotionNegative,
            "emotionSource": request.emotionSource,
            "note": request.note
        }

        doc_ref = db.collection('users').document(userId).collection('emotions').where('date', '==', datetime.combine(date.today(), datetime.min.time())).get()
        if len(list(doc_ref)) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Emotion for the date not found, please use POST to create a new one",
            )
        
        doc_ref = db.collection('users').document(userId).collection('emotions').document(doc_ref[0].id)

        data["lastUpdated"] = datetime.now()
        data["date"] = datetime.combine(data["date"], datetime.min.time())

        doc_ref.update(data)
        return DefaultResponse(
            message="Emotion updated successfully",
            data=data
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
@router.get("/user/{userId}/emotion", response_model=GetEmotion, status_code=status.HTTP_200_OK)
async def get_emotion(
    userId: str
):
    try:
        doc_ref = db.collection('users').document(userId).collection('emotions')
        docs = doc_ref.get()

        data = []

        for doc in docs:
            doc_data = doc.to_dict()
            data.append(doc_data)

        print(data)
        return GetEmotion(
            data=data
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )