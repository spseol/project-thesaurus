from typing import Type

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from apps.accounts import logger
from apps.accounts.models import User
from apps.utils.utils import keydefaultdict

_group_cache = keydefaultdict(lambda n: Group.objects.get_or_create(name=n)[0])


def sync_user_relations(user: User, attrs: dict):
    dn = attrs.get('distinguishedName')[0]

    user.is_active = True
    user.save(update_fields=['is_active'])

    dn_parts = dn.lower().split(',')
    if 'ou=zaci' in dn_parts:
        class_ = dn.split(',')[1].split('=')[1].replace(' ', '')
        user.school_class = class_

        user.groups.add(_group_cache['student'])
        user.save(update_fields=['school_class'])

    elif 'ou=ucitele' in dn_parts:
        user.groups.add(_group_cache['teacher'])

    elif 'ou=zaci-zakazani' in dn_parts:
        pass  # RIP

    else:
        logger.info("Not group assigned for user: %s.", dn_parts)


def clean_user_data(model_fields: dict) -> dict:
    username = model_fields.get('username')

    # type: Type[User]
    User = get_user_model()

    if User.objects.filter(username=username, first_name__isnull=False, last_name__isnull=False).exists():
        # do not refresh first&last name for users already present in database
        model_fields.pop('first_name', '')
        model_fields.pop('last_name', '')

    return model_fields
