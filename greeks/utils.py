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


def discount(start, end, asset, risk_free_rate, compounding):
    # TODO if (end - start) > term, rate is flat after
    if compounding.value() == Compounding.CONTINUOUS:
        # continuous compounding
        return asset.value() / (math.e) ** (1.0 + risk_free_rate.value() * ((end.value() - start.value()).total_seconds() / compounding.value().value))
    return asset.value() / (1.0 + risk_free_rate.value()) ** ((end.value() - start.value()).total_seconds() / compounding.value().value)
