from pydantic import BaseModel, Field
from uuid import UUID
from fastapi import Query
from datetime import date
from typing import List, Optional

class SingleFood(BaseModel):
    namaMakanan: str = Field(None, example="Nasi")
    porsi: str = Field(None, example="1 100 gram")
    kalori: int = Field(None, example=200)
    karbohidrat: int = Field(None, example=200)
    lemak: int = Field(None, example=200)
    serat: int = Field(None, example=200)
    protein: int = Field(None, example=200)

class PostFood(BaseModel):
    id: str
    date: date
    # lastUpdated: date
    asupanKalori: int = Field(None, example=2000)
    totalKarbohidrat: int = Field(None, example=200)
    totalLemak: int = Field(None, example=200)
    totalSerat: int = Field(None, example=200)
    totalProtein: int = Field(None, example=200)
    makanan: List[SingleFood]

class GetAllFood(BaseModel):
    food: List[PostFood]