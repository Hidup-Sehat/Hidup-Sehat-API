from pydantic import BaseModel, Field
from uuid import UUID
from fastapi import Query
from datetime import date
from typing import List

class GetAllActivity(BaseModel):
    id: UUID
    cardColor: int
    type: str
    category: str
    difficulty: str
    imgUrl: str
    movementCount: int

class GetActivityMovement(BaseModel):
    id: UUID
    # movementData: List[
    #     {
    #         sudutSikuKanan: int,
    #         sudutSikuKiri: int,
    #         sudutKetiakKanan: int,
    #         sudutKetiakKiri: int,
    #         sudutPundakKanan: int,
    #         sudutPundakKiri: int,
    #         sudutPinggulKanan: int,
    #         sudutPinggulKiri: int,
    #         sudutPahaKanan: int,
    #         sudutPahaKiri: int,
    #         sudutLututKanan: int,
    #         sudutLututKiri: int
    #     }
    # ]