from pydantic import BaseModel, Field
from uuid import UUID
from fastapi import Query
from datetime import date, datetime
from typing import List, Optional

class Emotion(BaseModel):
    id: int = Field(None, example=2)
    date: date
    lastUpdated: datetime
    emotionPositive: str = Field(None, example="Antusias,Gembira")
    emotionNegative: str = Field(None, example="Kecewa,Lesu")
    emotionSource: str = Field(None, example="Keluarga,Teman")
    note: str = Field(None, example="Saya merasa senang karena hari ini saya berhasil menyelesaikan tugas yang diberikan oleh dosen")

class GetEmotion(BaseModel):
    data: List[Emotion]