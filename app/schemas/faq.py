from pydantic import BaseModel, Field, conint
from uuid import UUID
from fastapi import Query
from datetime import date, datetime
from typing import List

class GetFAQ(BaseModel):
    id: str
    question: str
    answer: str