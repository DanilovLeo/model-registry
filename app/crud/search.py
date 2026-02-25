from typing import List, Optional
from tortoise.expressions import Q
from app.models.model import Model
from app.models.model_version import ModelVersion, Stage, Framework


async def search_models(
    q: Optional[str] = None,
    team_id: Optional[int] = None,
    framework: Optional[Framework] = None,
    stage: Optional[Stage] = None,
    tags: Optional[List[str]] = None,
) -> List[Model]:
    query = Model.filter(is_deleted=False)

    if q:
        query = query.filter(Q(name__icontains=q) | Q(description__icontains=q))

    if team_id:
        query = query.filter(team_id=team_id)

    models = await query.prefetch_related("versions").all()

    if framework or stage or tags:
        filtered_models = []
        for model in models:
            versions = await ModelVersion.filter(model_id=model.id, is_deleted=False).all()

            if framework:
                versions = [v for v in versions if v.framework == framework]
            if stage:
                versions = [v for v in versions if v.stage == stage]

            if tags:
                tag_filtered_versions = []
                for version in versions:
                    await version.fetch_related("tags")
                    version_tags = {f"{tag.key}:{tag.value}" for tag in version.tags}
                    if any(tag in version_tags for tag in tags):
                        tag_filtered_versions.append(version)
                versions = tag_filtered_versions

            if versions:
                filtered_models.append(model)

        return filtered_models

    return models
