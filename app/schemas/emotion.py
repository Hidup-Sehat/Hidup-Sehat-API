from pydantic import BaseModel, Field
from uuid import UUID
from fastapi import Query
from datetime import date

class GetUserEmotion(BaseModel):
    id: UUID
    emotion: str = Field(..., example="Happy")
    note: str

class CreateUserEmotion(BaseModel):
    date: date
    emotion: str = Query("", regex="^(Very Sad|Sad|OK|Happy|Very Happy)$")
    note: str