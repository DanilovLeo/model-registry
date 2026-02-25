from fastapi import APIRouter, Query
from typing import List, Optional
from app.schemas.model import ModelList
from app.models.model_version import Stage, Framework
from app.crud import search as search_crud

router = APIRouter(prefix="/api/v1/search", tags=["search"])


@router.get("", response_model=List[ModelList])
async def search_models(
    q: Optional[str] = Query(None, description="Search query for model name or description"),
    team_id: Optional[int] = Query(None, description="Filter by team ID"),
    framework: Optional[Framework] = Query(None, description="Filter by framework"),
    stage: Optional[Stage] = Query(None, description="Filter by stage"),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated, format: key:value)"),
):
    tag_list = None
    if tags:
        tag_list = [t.strip() for t in tags.split(",")]

    models = await search_crud.search_models(
        q=q,
        team_id=team_id,
        framework=framework,
        stage=stage,
        tags=tag_list,
    )
    return models
