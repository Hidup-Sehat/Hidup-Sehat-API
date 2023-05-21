from pydantic import BaseModel, Field
from uuid import UUID
from fastapi import Query
from datetime import date
from typing import List

class CreateUserDetail(BaseModel):
    id: UUID
    gender: str
    age: int
    height: int
    weight: int
    target: str
    weightTarget: int