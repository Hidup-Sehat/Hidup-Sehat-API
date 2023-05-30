from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.blog import (
    GetAllBlogs,
    GetBlog,
    BlogDetails
)
from app.deps.firebase import db

router = APIRouter()

@router.get("/blogs", response_model=GetAllBlogs, status_code=status.HTTP_200_OK)
async def get_all_blogs():
    try:
        blogs_ref = db.collection('blogs')
        query = blogs_ref.order_by('createdAt')
        docs = query.stream()

        blogs = []

        for doc in docs:
            data = doc.to_dict()
            title = data.get('title')
            slug = data.get('slug')
            imgUrl = data.get('imgUrl')
            createdAt = data.get('createdAt')
            tags = data.get('tags')

            blogs.append({
                'id': id,
                'title': title,
                'slug': slug,
                'imgUrl': imgUrl,
                'createdAt': createdAt,
                'tags': tags
            })

        return GetAllBlogs(
            message="All blogs retrieved",
            data=blogs
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.get("/blog/{blog_id}", response_model=GetBlog, status_code=status.HTTP_200_OK)
async def get_blog(blog_id: str):
    try:
        blog_ref = db.collection('blogs').document(blog_id)
        doc_snapshot = blog_ref.get()
        if not doc_snapshot.exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found",
            )
        data = doc_snapshot.to_dict()
        title = data.get('title')
        slug = data.get('slug')
        imgUrl = data.get('imgUrl')
        content = data.get('content')
        author = data.get('author')
        createdAt = data.get('createdAt')
        tags = data.get('tags')
        viewers = data.get('viewers')
        likes = data.get('likes')

        blog_details = BlogDetails(
            title=title,
            slug=slug,
            imgUrl=imgUrl,
            content=content,
            author=author,
            createdAt=createdAt,
            tags=tags,
            viewers=viewers,
            likes=likes
        )

        return GetBlog(
            message=f"Blog '{title}' retrieved",
            data=blog_details
        )

# Vt6VETF5zUPacVqKnsDB

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )