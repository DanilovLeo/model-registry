from typing import List, Optional
from app.models.model import Model
from app.schemas.model import ModelCreate


async def create_model(team_id: int, model_data: ModelCreate) -> Model:
    model = await Model.create(team_id=team_id, **model_data.model_dump())
    return model


async def get_model(model_id: int) -> Optional[Model]:
    return await Model.filter(id=model_id, is_deleted=False).first()


async def get_model_by_name(team_id: int, name: str) -> Optional[Model]:
    return await Model.filter(team_id=team_id, name=name, is_deleted=False).first()


async def get_models_by_team(team_id: int) -> List[Model]:
    return await Model.filter(team_id=team_id, is_deleted=False).all()


async def get_all_models() -> List[Model]:
    return await Model.filter(is_deleted=False).all()


async def delete_model(model_id: int) -> bool:
    model = await get_model(model_id)
    if not model:
        return False
    model.is_deleted = True
    await model.save()
    return True
