import re
from functools import partial

import unidecode
from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields.related import ForeignObjectRel, OneToOneRel
from rest_framework import filters
from rest_framework.filters import SearchFilter


class RelatedOrderingFilter(filters.OrderingFilter):
    """

    See: https://github.com/tomchristie/django-rest-framework/issues/1005

    Extends OrderingFilter to support ordering by fields in related models
    using the Django ORM __ notation
    """

    def is_valid_field(self, model, field):
        """
        Return true if the field exists within the model (or in the related
        model specified using the Django ORM __ notation)
        """
        components = field.split('__', 1)
        try:
            field = model._meta.get_field(components[0])

            if isinstance(field, OneToOneRel):
                return self.is_valid_field(field.related_model, components[1])

            # reverse relation
            if isinstance(field, ForeignObjectRel):
                return self.is_valid_field(field.model, components[1])

            # foreign key
            if field.remote_field and len(components) == 2:
                return self.is_valid_field(field.related_model, components[1])

            return True
        except FieldDoesNotExist:
            return False

    def remove_invalid_fields(self, queryset, fields, ordering, view):
        return [term for term in fields
                if self.is_valid_field(queryset.model, term.lstrip('-'))]


class UnAccentSearchFilter(SearchFilter):
    STRIP_FROM_SEARCH_FIELDS = re.compile(r'__unaccent')

    def get_search_terms(self, request):
        terms = super().get_search_terms(request=request)

        return tuple(map(unidecode.unidecode, terms))

    def must_call_distinct(self, queryset, search_fields):
        search_fields = map(partial(self.STRIP_FROM_SEARCH_FIELDS.sub, ''), search_fields)

        return super().must_call_distinct(queryset, search_fields)
