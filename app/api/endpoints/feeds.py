from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from app.deps.feed_recommendation import Recommendation
from app.schemas.feed import (
    GetFeeds,
    GetFeedUrl
)
from app.deps.firebase import db
import math
import json

router = APIRouter()

with open('app/api/data/database_blog.json') as file:
    data = json.load(file)

@router.post("/feeds", status_code=status.HTTP_200_OK)
async def get_feeds(
  request: GetFeeds,
  page: int = 1, limit: int = 10
):
  try:
    data_user = request.user_current_mood
    model = Recommendation(r'app/api/data/database_blog.json',str(data_user))
    recommendations = list(model.recomendations().itertuples(index=False, name=None))

    total_recommendations = len(recommendations)
    total_pages = math.ceil(total_recommendations / limit)

    start_index = (page - 1) * limit
    end_index = start_index + limit

    paginated_recommendations = recommendations[start_index:end_index]

    recommendation_list = [
      {
        'key': rec[0], 
        'title': rec[1], 
        'summary': rec[2],
        'imgUrl': rec[3], 
        'author': rec[5], 
        'createdAt': rec[6],
        'link': rec[8],
      }
      for rec in paginated_recommendations
    ]
    return {
      'data': recommendation_list,
      'page': page,
      'limit': limit,
      'totalRecommendations': total_recommendations,
      'totalPages': total_pages
    }

  except ValueError as e:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(e),
    )

@router.get("/feeds/{feed_id}", response_model=GetFeedUrl, status_code=status.HTTP_200_OK)
async def get_feed_url(
  feed_id: str
):
  try:
    for item in data:
      if item["id"] == feed_id:
        return GetFeedUrl(**item)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Feed not found",
    )

  except ValueError as e:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(e),
    )