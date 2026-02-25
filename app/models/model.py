from tortoise import fields
from tortoise.models import Model as TortoiseModel


class Model(TortoiseModel):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, index=True)
    description = fields.TextField(null=True)
    team = fields.ForeignKeyField("models.Team", related_name="models", on_delete=fields.CASCADE)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    is_deleted = fields.BooleanField(default=False)

    versions: fields.ReverseRelation["ModelVersion"]

    class Meta:
        table = "models"
        unique_together = (("name", "team"),)
