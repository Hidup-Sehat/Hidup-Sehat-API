from pydantic import BaseModel, Field
from uuid import UUID
from fastapi import Query
from datetime import date
from typing import List

class Register(BaseModel):
    id: UUID
    username: str
    email: str
    password: str
    confirmPassword: str

class Login(BaseModel):
    email: str
    password: str

class CreateUserDetail(BaseModel):
    uid: str = Field(..., example="e0c12eca-fb92-11ed-be56-0242ac120002")
    id: UUID
    email: str = Field(..., example="eds02@gmail.com")
    name: str
    imgUrl: str
    contactNumber: str
    dateOfBirth: date
    age: int = Field(..., example=21)
    gender: str | str = Query(..., regex="^(Male|Female)$")
    height: int = Field(..., example=170)
    weight: int = Field(..., example=70)
    target: str
    weightTarget: int = Field(..., example=65)

class UpdateProfile(BaseModel):
    id: UUID
    name: str
    dateOfBirth: date

class UpdatePassword(BaseModel):
    id: UUID
    password: str
    confirmPassword: str

class GetLeaderboard(BaseModel):
    id: UUID
    username: str
    name: str
    points: int