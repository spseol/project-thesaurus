from uuid import uuid4

from django.db.models import Model, UUIDField
from django.utils.translation import gettext as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField


class BaseModel(Model):
    """Base model with UUID primary key."""
    id = UUIDField(primary_key=True, default=uuid4, editable=True)

    class Meta:
        abstract = True


class BaseTimestampedModel(BaseModel):
    """Base model with stored creation and last modification date."""
    created = CreationDateTimeField(_('created'))
    modified = ModificationDateTimeField(_('modified'))

    def save(self, **kwargs):
        self.update_modified = kwargs.pop('update_modified', getattr(self, 'update_modified', True))
        super(BaseTimestampedModel, self).save(**kwargs)

    class Meta:
        get_latest_by = 'modified'
        ordering = ('-modified', '-created',)
        abstract = True
