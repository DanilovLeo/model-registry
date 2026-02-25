from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class TagCreate(BaseModel):
    key: str = Field(..., min_length=1, max_length=100)
    value: str = Field(..., min_length=1, max_length=255)


class TagResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    key: str
    value: str
    created_at: datetime
