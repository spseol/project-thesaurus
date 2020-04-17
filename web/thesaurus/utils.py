import os
import re


class Environment:
    """Helper class to access environmental variables"""

    def __init__(self, prefix='', strict=False):
        def _format_attr_name(name):
            result = re.sub(r'[^a-z0-9]', '_', name.lower())
            result = result[len(prefix):].strip('_')
            return result or name.lower()

        self._keys = {
            _format_attr_name(key): key
            for key in os.environ.keys()
            if key.startswith(prefix)
        }
        self.prefix = prefix
        self._strict = strict

    def __dir__(self):
        attrs = set(self._keys.keys()) | set(super().__dir__())
        return sorted(list(attrs))

    def __getattr__(self, name):
        try:
            if name in self._keys:
                value = os.environ.get(self._keys[name])
            else:
                value = os.environ[name]
            try:
                return int(value)
            except ValueError:
                return value

        except KeyError:
            if not self._strict:
                return ''
            msg = (
                f'{self.prefix.upper()}_{name.upper()} '
                f'not found in {dir(self)}'
            )
            raise AttributeError(msg)


__all__ = ['Environment']
