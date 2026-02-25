from tortoise import fields
from tortoise.models import Model


class Dataset(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, index=True)
    description = fields.TextField(null=True)
    path = fields.CharField(max_length=1024, null=True)
    metadata = fields.JSONField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    is_deleted = fields.BooleanField(default=False)

    model_versions: fields.ReverseRelation["ModelVersion"]

    class Meta:
        table = "datasets"
