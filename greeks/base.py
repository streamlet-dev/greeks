from datetime import datetime
import numpy as np
import pandas as pd
import tributary.lazy as tl

_ENV_CONTEXT = None


class Env(tl.LazyGraph):
    def __init__(self, now=None):
        self._now = now or datetime.now()
        self._override = None
        super().__init__()

    @tl.node()
    def now(self):
        self._now = datetime.now()
        return self._override if self._override is not None else self._now

    def override(self, val):
        self._override = val

    def reset(self):
        self._override = None


class Point(tl.LazyGraph):
    def __init__(self, name, env=_ENV_CONTEXT):
        self._name = name
        self._env = env or Env()
        self._now = self._env.now()
        super().__init__()

    def tt(self, val):
        self._env.override(val)

    def now(self):
        return self._now

    @tl.node()
    def value(self):
        return 0.0


class ExamplePoint(Point):
    def __init__(self, name="ExamplePt", env=_ENV_CONTEXT):
        super().__init__(name=name, env=_ENV_CONTEXT)

        _now = self.now()()
        self._curve = pd.util.testing.getTimeSeriesData(1000, 'H')['A']
        self._curve.index += pd.DateOffset(years=_now.year - 2000, months=_now.month - 1)

    @tl.node()
    def asof(self, date=None):
        if date is None:
            # return last
            return self._curve.iloc[-1]
        seq = self._curve[self._curve.index < date].index
        return np.nan if seq.empty else self._curve.loc[max(seq)]

    @tl.node(date="now")
    def price(self, date):
        return self.asof(date)

    def plot(self):
        self._curve.plot()
