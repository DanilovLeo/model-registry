from tortoise import fields
from tortoise.models import Model
from enum import Enum


class Stage(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"
    ARCHIVED = "ARCHIVED"


class Framework(str, Enum):
    PYTORCH = "pytorch"
    TENSORFLOW = "tensorflow"
    SKLEARN = "sklearn"
    XGBOOST = "xgboost"
    LIGHTGBM = "lightgbm"
    CATBOOST = "catboost"
    OTHER = "other"


class ModelVersion(Model):
    id = fields.IntField(pk=True)
    version = fields.CharField(max_length=100, index=True)
    model = fields.ForeignKeyField("models.Model", related_name="versions", on_delete=fields.CASCADE)

    artifact_path = fields.CharField(max_length=1024)
    stage = fields.CharEnumField(Stage, default=Stage.DEVELOPMENT, index=True)
    framework = fields.CharEnumField(Framework, default=Framework.OTHER, index=True)

    metrics = fields.JSONField(null=True)
    hyperparameters = fields.JSONField(null=True)
    dataset_info = fields.JSONField(null=True)

    dataset = fields.ForeignKeyField("models.Dataset", related_name="model_versions", null=True, on_delete=fields.SET_NULL)

    description = fields.TextField(null=True)
    created_by = fields.CharField(max_length=255, null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    is_deleted = fields.BooleanField(default=False)

    tags: fields.ManyToManyRelation["Tag"]

    class Meta:
        table = "model_versions"
        unique_together = (("version", "model"),)
