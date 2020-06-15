from datetime import datetime
import tributary.lazy as tl

_ENV_CONTEXT = None


class Env(tl.LazyGraph):
    def __init__(self, now=None):
        self._now = now or datetime.now()

    def now(self):
        return self._now


class Price(tl.LazyGraph):
    def __init__(self, name, now=_ENV_CONTEXT):
        self._name = name
