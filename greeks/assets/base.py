from ..base import Node, Timeseries
from ..utils import Compounding, discount


class Rate(Timeseries):
    def __init__(self, env):
        super().__init__(name="Rate", env=env)


class Equity(Timeseries):
    def __init__(self, env):
        super().__init__(name="Equity", env=env)


class Forward(Timeseries):
    def __init__(self, env, start, underlying, risk_free_rate, compounding=Compounding.YEARLY):
        self._start = start
        self._underlying = underlying
        self._risk_free_rate = risk_free_rate

        super().__init__(name="Forward",
                         env=env,
                         callable=discount,
                         callable_kwargs={"start": self._start.node(),
                                          "end": env.now(),
                                          "asset": self._underlying.node(),
                                          "risk_free_rate": self._risk_free_rate.node(),
                                          "compounding": Node(name="Compounding", value=compounding)})

