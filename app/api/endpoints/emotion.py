from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.default_schemas import DefaultResponse
from app.schemas.emotion import (
    Emotion,
    GetEmotionByDate
)
from datetime import date, datetime
from app.deps.firebase import db

router = APIRouter()

@router.post("/user/{user_uid}/emotion", status_code=status.HTTP_201_CREATED)
async def create_emotion(
    user_uid: str,
    request: Emotion
):
    try: 
        data = {
            # "id": request.id,
            "date": request.date,
            # "lastUpdated": datetime.now(),
            "emoji": request.emoji, # 1-5
            "emotionPositive": request.emotionPositive,
            "emotionNegative": request.emotionNegative,
            "emotionSource": request.emotionSource,
            "note": request.note
        }

        dateExist = db.collection('users').document(user_uid).collection('emotions').where('date', '==', datetime.combine(request.date, datetime.min.time())).get()
        if len(dateExist) > 0:
            doc_ref = db.collection('users').document(user_uid).collection('emotions').document(dateExist[0].id)
        else: 
            doc_ref = db.collection('users').document(user_uid).collection('emotions').document()

        data["id"] = doc_ref.id
        data["date"] = datetime.combine(request.date, datetime.min.time())
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
    
@router.get("/user/{user_uid}/emotion/{date}", response_model=GetEmotionByDate, status_code=status.HTTP_200_OK)
async def get_emotion(
    user_uid: str,
    date: date
):
    try:
        doc_ref = db.collection('users').document(user_uid).collection('emotions').where('date', '==', datetime.combine(date, datetime.min.time())).get()
        if len(list(doc_ref)) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Emotion for the date not found",
            )

        data = doc_ref[0].to_dict()

        return GetEmotionByDate(
            data=data
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
