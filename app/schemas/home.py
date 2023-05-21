from pydantic import BaseModel, Field
from uuid import UUID
from fastapi import Query
from datetime import date
from typing import List

class GetUserEmotion(BaseModel):
    emotion: str = Field(..., example="Happy")
    note: str

class GetUserStatistic(BaseModel):
    id: UUID
    actualCalorie: int
    CalorieNeeds: int
    actualWater: int
    WaterNeeds: int
    actualSleep: float
    SleepNeeds: float
    actualCalorieBurned: int
    CalorieBurnedNeeds: int
    emotionHistory: List[GetUserEmotion]

class UpdateUserStatisticTarget(BaseModel):
  CalorieNeeds: int
  CalorieBurnedNeeds: int
  SleepNeeds: float
  WaterNeeds: int


class CreateUserEmotion(BaseModel):
    date: date
    # emotion: str = Query("", regex="^(Very Sad|Sad|OK|Happy|Very Happy)$")
    emotion: str = Field(..., example="Happy")
    note: str