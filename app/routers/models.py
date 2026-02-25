from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.model import ModelCreate, ModelResponse, ModelList
from app.crud import team as team_crud
from app.crud import model as model_crud

router = APIRouter(prefix="/api/v1", tags=["models"])


@router.post("/teams/{team_id}/models", response_model=ModelResponse, status_code=status.HTTP_201_CREATED)
async def create_model(team_id: int, model: ModelCreate):
    team = await team_crud.get_team(team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {team_id} not found",
        )

    existing = await model_crud.get_model_by_name(team_id, model.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Model with name '{model.name}' already exists for team {team_id}",
        )

    created_model = await model_crud.create_model(team_id, model)
    return created_model


@router.get("/teams/{team_id}/models", response_model=List[ModelList])
async def list_team_models(team_id: int):
    team = await team_crud.get_team(team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {team_id} not found",
        )
    models = await model_crud.get_models_by_team(team_id)
    return models


@router.get("/models", response_model=List[ModelList])
async def list_all_models():
    models = await model_crud.get_all_models()
    return models


@router.get("/models/{model_id}", response_model=ModelResponse)
async def get_model(model_id: int):
    model = await model_crud.get_model(model_id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model with id {model_id} not found",
        )
    return model


@router.delete("/models/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_model(model_id: int):
    deleted = await model_crud.delete_model(model_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model with id {model_id} not found",
        )
