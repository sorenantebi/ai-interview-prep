"""Pure filtering helpers operating on lists of events."""


def upcoming(events, today):
    """Events that have not happened yet, i.e. taking place today or later."""
    return [event for event in events if event.day > today]


def in_range(events, start, end):
    """Events whose day lies between ``start`` and ``end``, both inclusive."""
    return [event for event in events if start <= event.day <= end]


def by_category(events, category):
    """Events in ``category`` (case-insensitive)."""
    wanted = category.lower()
    return [event for event in events if event.category.lower() == wanted]


def with_tag(events, tag):
    """Events carrying ``tag``."""
    return [event for event in events if event.has_tag(tag)]
