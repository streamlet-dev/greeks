from ..base import Timeseries
from ..utils import Compounding, discount_vs_starting


class Rate(Timeseries):
    def __init__(self, env=None, name="", value=None, at=None):
        super().__init__(name="Rate", env=env, value=value, at=at)


class Equity(Timeseries):
    def __init__(self, env=None, name="", value=None, at=None):
        super().__init__(name="Equity", env=env, value=value, at=at)


class Forward(Timeseries):
    def __init__(
        self, env, start, end, underlying, risk_free_rate, compounding=Compounding.YEARLY
    ):
        self._start = start
        self._end = end
        self._underlying = underlying
        self._risk_free_rate = risk_free_rate

        super().__init__(
            env=env,
            name="Forward",
            callable=discount_vs_starting,
            callable_kwargs={
                "start": self._start,
                "end": self._end,
                "now": env.now(),
                "asset": self._underlying,
                "risk_free_rate": self._risk_free_rate,
                "compounding": Timeseries(env=env, name="Compounding", value=compounding, at=start),
            },
        )
