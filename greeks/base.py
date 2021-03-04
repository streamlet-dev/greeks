from datetime import datetime

import numpy as np
import pandas as pd
from tributary.lazy import Node


class Env(object):
    def __init__(self, date: datetime = None) -> None:
        self._now = Point(name="Now")

    def now(self) -> Node:
        return self._now


class Point(Node):
    def __init__(self, timestamp: datetime = None, name: str = "Point") -> None:
        if timestamp:
            super().__init__(name=name, value=timestamp)
        else:
            super().__init__(name=name, callable=datetime.now)

    def node(self):
        """for symmetry"""
        return self


class Timeseries(object):
    def __init__(self, env=None, name="", callable=None, callable_kwargs=None):
        self._env = env or Env()
        self._curve = pd.Series(dtype=float, index=pd.DatetimeIndex([]))
        self._value = Node(
            name=name or "Point",
            callable=callable or (lambda dt_node: self._getLast(dt_node.eval())),
            callable_kwargs=callable_kwargs or {"dt_node": self._env.now()},
            dynamic=True,
        )

    def _getLast(self, dt):
        seq = self._curve[self._curve.index <= dt].index
        return np.nan if seq.empty else self._curve.loc[max(seq)]

    def node(self):
        return self._value

    def value(self, asof=None):
        if asof:
            self._env.now().setValue(asof)
            ret = self._value()
            self._env.now().unlock()
            return ret
        return self._value()

    def setValue(self, val, dt=None):
        dt = dt or self._env.now().eval()
        self._curve[dt] = val
        self._curve.sort_index(inplace=True)

    def values(self):
        return self._curve

    def plot(self):
        return self._curve.plot(drawstyle="steps-post")
