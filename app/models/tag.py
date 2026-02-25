from tortoise import fields
from tortoise.models import Model


class Tag(Model):
    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=100, index=True)
    value = fields.CharField(max_length=255, index=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    model_versions = fields.ManyToManyField("models.ModelVersion", related_name="tags", through="model_version_tags")

    class Meta:
        table = "tags"
        unique_together = (("key", "value"),)
