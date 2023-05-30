from pydantic import BaseModel, Field
from uuid import UUID
from fastapi import Query
from datetime import date
from typing import List

class BlogList(BaseModel):
    title: str
    slug: str
    imgUrl: str
    createdAt: date
    tags: List[str]

class BlogDetails(BaseModel):
    title: str
    slug: str
    imgUrl: str
    content: str
    author: str
    createdAt: date
    tags: List[str]
    viewers: int
    likes: int

class GetAllBlogs(BaseModel):
    message: str
    data: List[BlogList]

class GetBlog(BaseModel):
    message: str
    data: BlogDetails