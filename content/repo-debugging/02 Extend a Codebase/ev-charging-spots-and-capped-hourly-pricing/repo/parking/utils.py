"""Small helpers that do not depend on the rest of the package."""

import math
from datetime import datetime

SECONDS_PER_HOUR = 3600


def started_hours(start: datetime, end: datetime) -> int:
    """Return the number of started hours between two datetimes.

    A stay of 61 minutes counts as two hours. Zero or negative durations
    count as zero hours.
    """
    seconds = (end - start).total_seconds()
    if seconds <= 0:
        return 0
    return math.ceil(seconds / SECONDS_PER_HOUR)
