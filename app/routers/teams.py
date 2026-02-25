from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.team import TeamCreate, TeamResponse, TeamList
from app.crud import team as team_crud

router = APIRouter(prefix="/api/v1/teams", tags=["teams"])


@router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(team: TeamCreate):
    existing = await team_crud.get_team_by_name(team.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Team with name '{team.name}' already exists",
        )
    created_team = await team_crud.create_team(team)
    return created_team


@router.get("", response_model=List[TeamList])
async def list_teams():
    teams = await team_crud.get_teams()
    return teams


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(team_id: int):
    team = await team_crud.get_team(team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {team_id} not found",
        )
    return team


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: int):
    deleted = await team_crud.delete_team(team_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {team_id} not found",
        )
