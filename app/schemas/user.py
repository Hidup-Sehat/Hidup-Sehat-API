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
    id: UUID
    gender: str
    age: int
    height: int
    weight: int
    target: str
    weightTarget: int

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