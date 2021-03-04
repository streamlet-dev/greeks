import numpy as np
from greeks import ExamplePoint
from datetime import datetime


class TestUtils:
    def test_example_point(self):
        pt = ExamplePoint()
        assert np.isnan(pt.asof(datetime(2000, 1, 1)))

    def test_example_point(self):
        pt = ExamplePoint()
        _now = datetime.now()
        assert pt.asof(datetime(_now.year, _now.month, 1, 0, 30))() == pt._curve.iloc[0]
