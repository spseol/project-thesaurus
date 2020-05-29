from datetime import datetime

from django.utils.formats import get_format


def parse_date(value):
    """Parse date from string by DATE_INPUT_FORMATS of current language"""
    for item in get_format('DATE_INPUT_FORMATS'):
        try:
            return datetime.strptime(value, item).date()
        except (ValueError, TypeError):
            continue

    return None
