import decouple


class AutoConfig(decouple.AutoConfig):
    RE_EVAL = {'DOCKER_HOST', }

    def __call__(self, key, *args, **kwargs):
        value = super().__call__(key, *args, **kwargs)

        if value in self.RE_EVAL and (reevaluated := super().__call__(value, default=None)) is not None:
            return reevaluated

        return value
