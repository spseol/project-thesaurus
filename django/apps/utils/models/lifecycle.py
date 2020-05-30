from inspect import ismethod
from typing import Set

from django.utils.functional import cached_property
from django_lifecycle import LifecycleModelMixin as OriginalLifecycleModelMixin
from django_lifecycle.utils import get_unhookable_attribute_names


# TODO: remove after merge of https://github.com/rsinger86/django-lifecycle/pull/48
class LifecycleModelMixin(OriginalLifecycleModelMixin):
    @cached_property
    def _potentially_hooked_methods(self):
        skip = set(get_unhookable_attribute_names(self)) | self._skipped_for_hooks
        collected = []

        for name in self.__class__.__dict__:
            if name in skip:
                continue
            try:
                attr = getattr(self, name)
                if ismethod(attr) and hasattr(attr, "_hooked"):
                    collected.append(attr)
            except AttributeError:
                pass

        return collected

    @cached_property
    def _skipped_for_hooks(self) -> Set[str]:
        return set()
