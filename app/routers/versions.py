from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.model_version import (
    ModelVersionCreate,
    ModelVersionResponse,
    ModelVersionList,
    StageUpdate,
)
from app.crud import model as model_crud
from app.crud import model_version as version_crud

router = APIRouter(prefix="/api/v1/models", tags=["versions"])


@router.post("/{model_id}/versions", response_model=ModelVersionResponse, status_code=status.HTTP_201_CREATED)
async def create_version(model_id: int, version: ModelVersionCreate):
    model = await model_crud.get_model(model_id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model with id {model_id} not found",
        )

    existing = await version_crud.get_model_version_by_version(model_id, version.version)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Version '{version.version}' already exists for model {model_id}",
        )

    created_version = await version_crud.create_model_version(model_id, version)
    return created_version


@router.get("/{model_id}/versions", response_model=List[ModelVersionList])
async def list_versions(model_id: int):
    model = await model_crud.get_model(model_id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model with id {model_id} not found",
        )
    versions = await version_crud.get_model_versions(model_id)
    return versions


@router.get("/{model_id}/versions/{version_id}", response_model=ModelVersionResponse)
async def get_version(model_id: int, version_id: int):
    version = await version_crud.get_model_version(version_id)
    if not version or version.model_id != model_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Version with id {version_id} not found for model {model_id}",
        )
    return version


@router.patch("/{model_id}/versions/{version_id}/stage", response_model=ModelVersionResponse)
async def update_version_stage(model_id: int, version_id: int, stage_update: StageUpdate):
    version = await version_crud.get_model_version(version_id)
    if not version or version.model_id != model_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Version with id {version_id} not found for model {model_id}",
        )

    updated_version = await version_crud.update_version_stage(version_id, stage_update.stage)
    return updated_version


@router.delete("/{model_id}/versions/{version_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_version(model_id: int, version_id: int):
    version = await version_crud.get_model_version(version_id)
    if not version or version.model_id != model_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Version with id {version_id} not found for model {model_id}",
        )

    deleted = await version_crud.delete_model_version(version_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Version with id {version_id} not found",
        )
