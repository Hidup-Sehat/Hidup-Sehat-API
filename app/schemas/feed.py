from pydantic import BaseModel, Field, conint
from uuid import UUID
from fastapi import Query
from datetime import date
from typing import List

class GetFeeds(BaseModel):
  user_current_mood: str = Field(..., example="hari ini aku {emosi postif, emosi negatif} yang berasal dari {asal emosi}, {cerita}")

class GetFeedUrl(BaseModel):
  title: str
  link: str