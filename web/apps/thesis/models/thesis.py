from uuid import uuid4

from django.db.models import Model, UUIDField


# TODO move to utils app
class BaseModel(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=True)

    class Meta:
        abstract = True


# TODO fill all required fields
class Thesis(BaseModel):
    pass
