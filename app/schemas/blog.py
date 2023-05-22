from pydantic import BaseModel, Field
from uuid import UUID
from fastapi import Query
from datetime import date
from typing import List

class getAllBlog(BaseModel):
    id: UUID
    title: str
    slug: str
    imgUrl: str
    createdAt: date
    tags: List[str]

class getBlog(BaseModel):
    id: UUID
    title: str
    slug: str
    imgUrl: str
    content: str
    author: str
    createdAt: date
    tags: List[str]
    viewers: int
    likes: int