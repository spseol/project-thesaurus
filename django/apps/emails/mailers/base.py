from abc import ABC
from contextlib import contextmanager
from operator import attrgetter, methodcaller
from typing import Iterable, ContextManager

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.template import Template
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _, override
from mailqueue.models import MailerMessage

from apps.accounts.models import User
from apps.emails import logger


class BaseMailer(ABC):
    @staticmethod
    @contextmanager
    def _new_message() -> ContextManager[MailerMessage]:
        email = MailerMessage()
        email.from_address = settings.DEFAULT_FROM_EMAIL

        try:
            with override(settings.EMAIL_LANGUAGE):
                yield email
        except:
            raise
        else:
            if email.html_content and not email.content:
                email.content = strip_tags(email.html_content)

            if not email.to_address:
                logger.warning('Email %s has not set recipient address.', email.subject)

            email.save()

    @classmethod
    def _render_content(cls, template_name: str, **context) -> str:
        template: Template = get_template(template_name)
        rendered = template.render(
            context=dict(
                title=settings.MAIL_SUBJECT_TITLE,
                **context,
            )
        )
        return '\n'.join(map(methodcaller('strip'), rendered.strip().split('\n')))

    @classmethod
    def _build_subject(cls, title: str) -> str:
        return _('{} | {}').format(settings.MAIL_SUBJECT_TITLE, title)

    @classmethod
    def _build_to_address(cls, users: Iterable[User]) -> str:
        return ', '.join(map(str, filter(cls._is_email, map(attrgetter('email'), users))))

    @staticmethod
    def _is_email(email: str) -> bool:
        try:
            validate_email(value=email)
            return True
        except ValidationError:
            return False
