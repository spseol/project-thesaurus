from collections import defaultdict
from typing import Callable, Any

from django.contrib.auth.models import Group

from apps.accounts import logger
from apps.accounts.models import User


class keydefaultdict(defaultdict):
    default_factory: Callable[[str], Any]

    # TODO: remove after feature/audit-log merge
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)

        ret = self[key] = self.default_factory(key)
        return ret


_group_cache = keydefaultdict(lambda n: Group.objects.get_or_create(name=n)[0])


def sync_user_relations(user: User, attrs: dict):
    dn = attrs.get('distinguishedName')[0]

    user.is_active = True
    user.save(update_fields=['is_active'])

    dn_parts = dn.lower().split(',')
    if 'ou=zaci' in dn_parts:
        class_ = dn.split(',')[1].split('=')[1]
        user.school_class = class_

        user.groups.add(_group_cache['student'])
        user.save(update_fields=['school_class'])

    elif 'ou=ucitele' in dn_parts:
        user.groups.add(_group_cache['teacher'])

    elif 'ou=zaci-zakazani' in dn_parts:
        pass  # RIP

    else:
        logger.info("Not group assigned for user: %s.", dn_parts)
