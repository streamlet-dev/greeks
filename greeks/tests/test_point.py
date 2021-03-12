import greeks as gk
import numpy as np
from datetime import datetime, timedelta


today = datetime.today()
tomorrow = today + timedelta(days=1)
env = gk.Env(today)

class TestPoint:
    def test_point(self):
        pt = gk.Point(env=env)
        print(pt())
        assert pt() == today
        assert pt.isDirty() == False

    def test_point_timestamp(self):
        pt = gk.Point(env=env, at=tomorrow)
        print(pt())
        assert pt() == tomorrow
        assert pt.isDirty() == False

    def test_point_value(self):
        pt = gk.Point(env=env, value=5)
        print(pt())
        assert pt() == 5
        assert pt.isDirty() == False

    def test_point_timestamp_and_value(self):
        pt = gk.Point(env=env, value=5, at=tomorrow)
        print(pt(at=today))
        print(pt())
        assert np.isnan(pt())
        assert pt.isDirty() == False

        print(pt(at=tomorrow))
        assert pt(at=tomorrow) == 5

        # FIXME args should apply as tweaks, not sets
        # assert np.isnan(pt())

    def test_previous(self):
        e = gk.Env(datetime.now())
        pt = gk.Point(e)
        assert np.isnan(pt.previous()[0])

        assert pt.previous(datetime.now())[0] == e.now().eval()
