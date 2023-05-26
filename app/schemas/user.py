from pydantic import BaseModel, Field
from uuid import UUID
from fastapi import Query
from datetime import date
from typing import List, Optional

class GetUserData(BaseModel):
    user_id: str
    username: str
    email: str

class RequestRegister(BaseModel):
    username: str
    email: str
    password: str
    confirmPassword: str

class ResponseRegister(BaseModel):
    message: str
    data: GetUserData

class RequestLogin(BaseModel):
    email: str
    password: str

class ResponseLogin(BaseModel):
    message: str
    data: GetUserData

class CreateUserDetail(BaseModel):
    # id: UUID
    # email: Optional[str] = Field(None, example="eds02@gmail.com")
    name: Optional[str]
    # imgUrl: Optional[str]
    contactNumber: Optional[str]
    dateOfBirth: Optional[date]
    age: Optional[int] = Field(None, example=21)
    gender: Optional[str] = Query(None, regex="^(Male|Female)$")
    height: Optional[int] = Field(None, example=170)
    weight: Optional[int] = Field(None, example=70)
    target: Optional[str]
    weightTarget: Optional[int] = Field(None, example=65)

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