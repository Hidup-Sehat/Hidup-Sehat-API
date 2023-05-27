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
    username: Optional[str] = Field(None, example="eds02")
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
    # id: UUID
    name: Optional[str] = Field(None, regex="^[a-z]{1,10}$")
    contactNumber: Optional[str] = Field(None, regex="^(\+62|0)[0-9]{8,15}$")
    dateOfBirth: Optional[date] = Field(None, example="2000-01-01")
    imgUrl: Optional[str] = Field(None, regex="^(http|https)://")

class UpdatePassword(BaseModel):
    id: UUID
    password: str
    confirmPassword: str


class LeaderboardEntry(BaseModel):
    username: str
    name: str
    points: int

class GetLeaderboard(BaseModel):
    data: List[LeaderboardEntry]
