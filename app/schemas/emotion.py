from pydantic import BaseModel, Field
from uuid import UUID
from fastapi import Query
from datetime import date
from typing import List, Optional

class Emotion(BaseModel):
    id: str = Field(None, example="1")
    date: date
    lastUpdated: date
    emotionPositive: str = Field(None, example="Antusias,Gembira")
    emotionNegative: str = Field(None, example="Kecewa,Lesu")
    emotionSource: str = Field(None, example="Keluarga,Teman")
    note: str = Field(None, example="Saya merasa senang karena hari ini saya berhasil menyelesaikan tugas yang diberikan oleh dosen")

class GetEmotion(BaseModel):
    data: List[Emotion]