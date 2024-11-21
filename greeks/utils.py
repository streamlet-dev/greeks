import math
from enum import Enum


class Compounding(Enum):
    CONTINUOUS = -1
    SECOND = 1
    MINUTE = 60
    HOUR = MINUTE * 60
    DAILY = HOUR * 24
    WEEKLY = DAILY * 7
    MONTHLY = DAILY * 30
    YEARLY = DAILY * 365


def discount(start, end, now, asset, risk_free_rate, compounding):
    # Take the minimum of now and end
    asof = min(end.value(), now.value())

    # spot price of asset
    asset_value = asset.value(at=start.value())

    # risk free rate agreed at start
    rfr = risk_free_rate.value(at=start.value())

    # compounding agreed at start
    compounding_value = compounding.value(at=start.value())

    # compounding is agreed at the start time, so take that value
    if compounding_value == Compounding.CONTINUOUS:
        # continuous compounding based on spot price of asset
        return asset_value / (math.e) ** (
            1.0
            + rfr * ((asof - start.value()).total_seconds() / compounding_value.value)
        )
    # return normal compounding of asset
    return asset_value / (1.0 + rfr) ** (
        (asof - start.value()).total_seconds() / compounding_value.value
    )


def discount_vs_starting(start, end, now, asset, risk_free_rate, compounding):
    # TODO if (end - start) > term, rate is flat after
    return discount(start, end, now, asset, risk_free_rate, compounding) - asset.value(
        at=start.value()
    )
