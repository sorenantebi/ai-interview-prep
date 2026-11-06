"""Exponential backoff arithmetic."""


def compute_delay(retry_number, base, factor, max_delay):
    """Seconds to wait before retry number ``retry_number`` (1 = first retry).

    The delay starts at ``base`` and is multiplied by ``factor`` for every
    further retry. It never exceeds ``max_delay``.
    """
    if retry_number < 1:
        raise ValueError("retry_number starts at 1")
    delay = base * factor ** (retry_number - 1)
    return min(delay, max_delay)
