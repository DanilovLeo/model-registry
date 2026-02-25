from typing import List, Optional
from app.models.model_version import ModelVersion, Stage
from app.models.tag import Tag
from app.schemas.model_version import ModelVersionCreate


async def create_model_version(model_id: int, version_data: ModelVersionCreate) -> ModelVersion:
    data = version_data.model_dump(exclude={"tag_ids"})
    data["model_id"] = model_id

    version = await ModelVersion.create(**data)

    if version_data.tag_ids:
        tags = await Tag.filter(id__in=version_data.tag_ids).all()
        await version.tags.add(*tags)

    return version


async def get_model_version(version_id: int) -> Optional[ModelVersion]:
    return await ModelVersion.filter(id=version_id, is_deleted=False).prefetch_related("tags").first()


async def get_model_version_by_version(model_id: int, version: str) -> Optional[ModelVersion]:
    return await ModelVersion.filter(model_id=model_id, version=version, is_deleted=False).first()


async def get_model_versions(model_id: int) -> List[ModelVersion]:
    return await ModelVersion.filter(model_id=model_id, is_deleted=False).all()


async def update_version_stage(version_id: int, stage: Stage) -> Optional[ModelVersion]:
    version = await get_model_version(version_id)
    if not version:
        return None
    version.stage = stage
    await version.save()
    return version


async def delete_model_version(version_id: int) -> bool:
    version = await get_model_version(version_id)
    if not version:
        return False
    version.is_deleted = True
    await version.save()
    return True
