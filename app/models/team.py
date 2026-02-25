from tortoise import fields
from tortoise.models import Model


class Team(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True, index=True)
    description = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    is_deleted = fields.BooleanField(default=False)

    models: fields.ReverseRelation["Model"]

    class Meta:
        table = "teams"
