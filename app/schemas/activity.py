from pydantic import BaseModel, Field
from uuid import UUID
from fastapi import Query
from datetime import date
from typing import List, Optional

class GetActivityMovement(BaseModel):
    id: int
    sudutSikuKanan: int
    sudutSikuKiri: int
    sudutKetiakKanan: int
    sudutKetiakKiri: int
    sudutPundakKanan: int
    sudutPundakKiri: int
    sudutPinggulKanan: int
    sudutPinggulKiri: int
    sudutPahaKanan: int
    sudutPahaKiri: int
    sudutLututKanan: int
    sudutLututKiri: int
    
class GetMovementList(BaseModel):
    movementName: str
    movementDesc: str
    imgUrl: str
    movementData: GetActivityMovement

class GetActivity(BaseModel):
    id: str
    cardColor: int
    type: str
    category: str
    difficulty: str
    imgUrl: str
    caloriesBurned: int
    movementCount: int
    movementList: List[GetMovementList]

class CreateActivity(BaseModel):
    id: str
    cardColor: int = Query(..., ge=1, le=4)
    type: str = Query(..., regex="^Yoga|Workout|Silat")
    category: str = Query(..., regex="^Kelenturan|Kekuatan|Keseimbangan")
    difficulty: str = Query(..., regex="^Pemula|Menengah|Ahli")
    imgUrl: str
    caloriesBurned: int = Field(None, example=100)
    movementCount: int = Field(None, example=5)
    movementList: List[GetMovementList]

class GetAllActivity(BaseModel):
    activity: List[GetActivity] 

class GetAllActivityMovement(BaseModel):
    movement: List[GetActivityMovement]