from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.blog import (
    getAllBlog,
    getBlog
)

router = APIRouter()

@router.get("/blogs", response_model=getAllBlog, status_code=status.HTTP_200_OK)
async def get_all_blogs():
    return {"message": "This is the All Blog endpoint"}

@router.get("/blog/{blog_id}", response_model=getBlog, status_code=status.HTTP_200_OK)
async def get_blog(blog_id: str):
    return {"message": "This is the Blog endpoint"}
    