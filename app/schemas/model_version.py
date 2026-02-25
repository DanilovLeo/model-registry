from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any, List
from app.models.model_version import Stage, Framework


class ModelVersionCreate(BaseModel):
    version: str = Field(..., min_length=1, max_length=100)
    artifact_path: str = Field(..., min_length=1, max_length=1024)
    stage: Optional[Stage] = Stage.DEVELOPMENT
    framework: Optional[Framework] = Framework.OTHER
    metrics: Optional[Dict[str, Any]] = None
    hyperparameters: Optional[Dict[str, Any]] = None
    dataset_info: Optional[Dict[str, Any]] = None
    dataset_id: Optional[int] = None
    description: Optional[str] = None
    created_by: Optional[str] = None
    tag_ids: Optional[List[int]] = None


class ModelVersionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    version: str
    model_id: int
    artifact_path: str
    stage: Stage
    framework: Framework
    metrics: Optional[Dict[str, Any]]
    hyperparameters: Optional[Dict[str, Any]]
    dataset_info: Optional[Dict[str, Any]]
    dataset_id: Optional[int]
    description: Optional[str]
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime


class ModelVersionList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    version: str
    model_id: int
    stage: Stage
    framework: Framework
    created_at: datetime


class StageUpdate(BaseModel):
    stage: Stage
