from pydantic.main import BaseModel
from typing import Optional

class DefaultResponse(BaseModel):
    message: str