from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DrfValidationError

from rest_framework.views import exception_handler as drf_exception_handler


def transform_exception(exception):
    """Transform model validation errors into an equivalent DRF ValidationError.
    After reading the references, you may decide not to use this.

    References:
    https://www.kye.id.au/blog/understanding-django-rest-framework-model-full-clean/
    https://www.dabapps.com/blog/django-models-and-encapsulation/

    https://gist.github.com/twidi/9d55486c36b6a51bdcb05ce3a763e79f
    """
    if isinstance(exception, DjangoValidationError):
        detail = None
        if hasattr(exception, "message_dict"):
            detail = exception.message_dict
        elif hasattr(exception, "message"):
            detail = exception.message
        elif hasattr(exception, "messages"):
            detail = exception.messages

        exception = DrfValidationError(detail=detail)

    return exception


def exception_handler(exc, context):
    """Handle Django ValidationError as an accepted exception
    Must be set in settings:
    >>> REST_FRAMEWORK = {
    ...     # ...
    ...     'EXCEPTION_HANDLER': '....exception_handler',
    ...     # ...
    ... }
    For the parameters, see ``exception_handler``
    """
    return drf_exception_handler(transform_exception(exc), context)
