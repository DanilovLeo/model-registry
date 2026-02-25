from typing import List, Optional
from app.models.team import Team
from app.schemas.team import TeamCreate


async def create_team(team_data: TeamCreate) -> Team:
    team = await Team.create(**team_data.model_dump())
    return team


async def get_team(team_id: int) -> Optional[Team]:
    return await Team.filter(id=team_id, is_deleted=False).first()


async def get_team_by_name(name: str) -> Optional[Team]:
    return await Team.filter(name=name, is_deleted=False).first()


async def get_teams() -> List[Team]:
    return await Team.filter(is_deleted=False).all()


async def delete_team(team_id: int) -> bool:
    team = await get_team(team_id)
    if not team:
        return False
    team.is_deleted = True
    await team.save()
    return True
