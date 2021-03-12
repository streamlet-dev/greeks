from datetime import datetime

import numpy as np
import pandas as pd
from tributary.lazy import Node
from typing import Any


class Env(object):
    '''An `Env` is a collection of tributary nodes
    representing configurable global graph values.

    It is designed to hold "true globals", such as current time
    '''
    def __init__(self, now: datetime = None) -> None:
        self._now = Node(name="Now", callable=lambda: datetime.now(), dynamic=True)
        if now:
            self._now.setValue(now)

    def now(self) -> Node:
        return self._now


class Point(Node):
    def __init__(self, env, value: Any = None, at: datetime = None, name: str = "Point") -> None:
        '''Point constructor.

        if `value` and `at` are defined, series will be value@at
        if `value` is defined, series will be value@now
        if `at` is defined, series will be at@at
        if neither defined, series is now@now

        Args:
            env (Env): graph env
            value (Any, optional): value in timeseries
            at (datetime, optional): date of the value
            name (str, optional): name of series
        '''

        # always instantiate an env
        self._env = env

        if at is not None:
            # use as index
            if isinstance(at, Point):
                index = pd.DatetimeIndex([at.eval()])
            else:
                index = pd.DatetimeIndex([at])

            # set as default node value
            callable_kwargs = {"at": at}
        else:
            # use env now value as index
            index = pd.DatetimeIndex([self._env.now().eval()])

            # use env now as value
            callable_kwargs = {"at": env.now()}

        if value is not None:
            # use data as value
            values = [value]

        else:
            # else use timestamp
            values = [index[0]]

        self._curve = pd.Series(values, index=index)
        super().__init__(name=name, callable=self._get, callable_kwargs=callable_kwargs)

    def _get(self, at):
        '''this is the node-wrapped function. it accesses a series'''
        try:
            # get sequence that is later than the time
            seq = self._curve[self._curve.index <= at.value()].index

            # if its empty, it means the value was not defined at that time
            return np.nan if seq.empty else self._curve.loc[max(seq)]
        except TypeError as e:
            print("Value in series is nan! From {}".format(self))
            raise e
        except Exception as e:
            print("error in {}".format(self))
            raise e

    def previous(self, at=None):
        '''get value before `at` or env.now(). returns tuple of (value, timestamp)'''
        at = at or self._env.now().eval()

        # get sequence that is later than the time
        seq = self._curve[self._curve.index < at]

        if seq.empty:
            # no previous value
            return (np.nan, datetime.fromtimestamp(0))

        return seq.index[-1], seq.iloc[-1]

    def value(self, at=None):
        '''get value. if `at`, will get as of that time. otherwise, will get as of env.now'''
        if at:
            # tweak and return
            return self(at=at)

        # return node value
        return super().value()

    def setValue(self, value=None, at=None):
        '''override value of series at a given time'''
        # use provided timestamp or now
        at = at or self._env.now().eval()

        if not value and not at:
            return
        elif not value:
            value = at

        # set value in curve
        self._curve[at] = value

        # resort curve by index
        self._curve.sort_index(inplace=True)

        # mark myself as dirty
        super().setValue(value)
        # self._dirty = True

    def values(self):
        '''return series'''
        return self._curve

    def plot(self):
        '''plot series'''
        return self._curve.plot(drawstyle="steps-post")


class Timeseries(Point):
    def __init__(self, env, name="", value=None, at=None, callable=None, callable_kwargs=None):
        self._env = env or Env()
        self._curve = pd.Series([value], index=pd.DatetimeIndex([at.value()])) if at and value else pd.Series(dtype=float, index=pd.DatetimeIndex([]))
        super(Point, self).__init__(
            name=name or "Point",
            callable=callable or self._get,
            callable_kwargs=callable_kwargs or {"at": at if at else self._env.now()},
            dynamic=True,
        )
