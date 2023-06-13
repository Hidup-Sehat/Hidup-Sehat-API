from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.faq import (
    GetFAQ
)
from datetime import datetime
from app.deps.firebase import db

router = APIRouter()

@router.get("/faq", response_model=list[GetFAQ], status_code=status.HTTP_200_OK)
async def get_faq():
    try:
      faq_collection = db.collection('faq')
      faq_items = faq_collection.stream()
      faqs = []
      for faq_item in faq_items:
          faq_data = faq_item.to_dict()
          faqs.append(faq_data)
      return faqs

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )