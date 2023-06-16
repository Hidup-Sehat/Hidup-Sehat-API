from pydantic import BaseModel, Field, conint
from uuid import UUID
from fastapi import Query
from datetime import date, datetime
from typing import List

class GetUserEmotion(BaseModel):
    emotion: conint(ge=1, le=5, strict=True)
    note: str

class GetUserDetail(BaseModel):
    id: str
    username: str
    name: str
    email: str
    imgUrl: str
    contactNumber: str
    dateOfBirth: datetime
    age: int
    gender: str
    height: int
    weight: int 
    target: str
    weightTarget: int
    registeredAt: datetime
    actualCalorie: int
    actualWater: int
    actualSleep: float
    calorieNeeds: int
    calorieBurned: int
    waterNeeds: float
    sleepNeeds: float
    # actualCalorieBurned: int
    # CalorieBurnedNeeds: int
    # emotionHistory: List[GetUserEmotion]
    # foodHistory: List[GetUserFood]

class UpdateUserStatistic(BaseModel):
    actualWater: int
    actualSleep: float

class CreateUserEmotion(BaseModel):
    date: date
    # emotion: str = Query("", regex="^(Very Sad|Sad|OK|Happy|Very Happy)$")
    emotion: conint(ge=1, le=5, strict=True)
    note: str