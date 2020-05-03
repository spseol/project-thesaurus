from uuid import uuid4

from django.db.models import Model, UUIDField, CharField, TextField, PositiveSmallIntegerField
from django.utils.translation import gettext as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

from apps.utils.models.managers import BaseTypeModelManager


class BaseModel(Model):
    """Base model with UUID primary key."""
    id = UUIDField(primary_key=True, default=uuid4, editable=False)

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


class BaseTypeModel(BaseModel):
    """Base model for Type* model enumerations."""
    identifier = CharField(
        verbose_name=_('Identifier'),
        unique=True,
        max_length=128,
        null=True,
        blank=True
    )
    name = CharField(
        verbose_name=_('Name'),
        max_length=256
    )
    description = TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True
    )
    order = PositiveSmallIntegerField(
        verbose_name=_('Order'),
    )

    objects = BaseTypeModelManager()

    class Meta:
        ordering = "order",
        abstract = True

    def __str__(self):
        return self.name or self.get_identifier_display()
