from typing import List, Optional
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetCreate


async def create_dataset(dataset_data: DatasetCreate) -> Dataset:
    dataset = await Dataset.create(**dataset_data.model_dump())
    return dataset


async def get_dataset(dataset_id: int) -> Optional[Dataset]:
    return await Dataset.filter(id=dataset_id, is_deleted=False).first()


async def get_datasets() -> List[Dataset]:
    return await Dataset.filter(is_deleted=False).all()


async def delete_dataset(dataset_id: int) -> bool:
    dataset = await get_dataset(dataset_id)
    if not dataset:
        return False
    dataset.is_deleted = True
    await dataset.save()
    return True
