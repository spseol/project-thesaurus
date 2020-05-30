from collections import defaultdict
from datetime import datetime

from django.utils.formats import get_format


class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


def parse_date(value):
    """Parse date from string by DATE_INPUT_FORMATS of current language"""
    for item in get_format('DATE_INPUT_FORMATS'):
        try:
            return datetime.strptime(value, item).date()
        except (ValueError, TypeError):
            continue

    return None
