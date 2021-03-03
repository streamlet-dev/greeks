from datetime import datetime
import numpy as np
import pandas as pd
import tributary.lazy as tl

_ENV_CONTEXT = None


class Env(object):
    def __init__(self, date=None):
        self._now = tl.Node(name="Env", callable=lambda: datetime.now())

    def now(self):
        return self._now


class Point(object):
    def __init__(self, env=None, name="", callable=None, callable_kwargs=None):
        self._env = env or Env()
        self._curve = pd.Series(dtype=float, index=pd.DatetimeIndex([]))
        self._value = tl.Node(name=name or "Point",
                              callable=callable or (lambda dt_node: self._getLast(dt_node.eval())),
                              callable_kwargs=callable_kwargs or {"dt_node": self._env.now()})

    def _getLast(self, dt):
        seq = self._curve[self._curve.index < dt].index
        return np.nan if seq.empty else self._curve.loc[max(seq)]

    def node(self):
        return self._value

    def value(self):
        return self._value()

    def setValue(self, val, dt=None):
        dt = dt or self._env.now().eval()
        self._curve[dt] = val
        self._curve.sort_index(inplace=True)

    def values(self):
        return self._curve

    def plot(self):
        return self._curve.plot()
