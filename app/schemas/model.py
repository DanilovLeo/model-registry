from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class ModelCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class ModelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    team_id: int
    created_at: datetime
    updated_at: datetime


class ModelList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    team_id: int
