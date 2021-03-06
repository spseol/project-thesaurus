from uuid import uuid4

from django.db.models import Model, UUIDField, CharField, PositiveSmallIntegerField
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

from apps.utils.models.managers import BaseTypeModelManager
from .lifecycle import LifecycleModelMixin


class BaseModel(Model):
    """Base model with UUID primary key."""
    id = UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class BaseTimestampedModel(LifecycleModelMixin, BaseModel):
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
        blank=True,
        choices=(),
    )
    order = PositiveSmallIntegerField(
        verbose_name=_('Order'),
        default=0,
    )

    objects = BaseTypeModelManager()

    class Meta:
        ordering = "order",
        abstract = True

    def __str__(self):
        # assuming choices on identifier
        return self.get_identifier_display()
