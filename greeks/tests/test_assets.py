import greeks as gk
from datetime import datetime, timedelta


class TestForward:
    def test_forward(self):
        e = gk.Env(now=datetime.today())
        start = gk.Point(env=e, at=e.now().eval() - timedelta(days=365), name="Start")
        end = gk.Point(env=e, at=e.now().eval() + timedelta(days=365), name="End")

        e.now().setValue(start())
        rfr = gk.Rate(env=e, value=0.05, at=start)
        asset = gk.Equity(env=e, value=200, at=start)
        n = gk.Forward(
            env=e, start=start, end=end, underlying=asset, risk_free_rate=rfr
        )

        assert -0.0001 < n() < 0.0001

        e.now().setValue(datetime.today())

        assert -9.53 < n() < -9.52

        rfr.setValue(0.10, at=start())

        assert -18.2 < n() < -18.1
