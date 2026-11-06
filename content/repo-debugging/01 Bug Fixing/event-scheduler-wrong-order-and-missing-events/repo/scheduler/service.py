"""The Scheduler service: stores events and answers calendar queries."""

from datetime import date

from scheduler import filters
from scheduler.formatting import format_agenda


def _sort_key(event):
    return (event.date, event.title.lower())


class Scheduler:
    """In-memory collection of events."""

    def __init__(self):
        self._events = []

    def __len__(self):
        return len(self._events)

    def add(self, event):
        """Add an event after validating its date; returns the event."""
        event.day  # raises ValueError for malformed dates
        self._events.append(event)
        return event

    def add_many(self, events):
        for event in events:
            self.add(event)

    def remove(self, title):
        """Remove every event with exactly this title; returns how many."""
        kept = [event for event in self._events if event.title != title]
        removed = len(self._events) - len(kept)
        self._events = kept
        return removed

    def sorted_events(self, reverse=False):
        """All events in chronological order (ties broken by title)."""
        return sorted(self._events, key=_sort_key, reverse=reverse)

    def upcoming(self, today=None, limit=None):
        """Events happening today or later, soonest first."""
        today = today or date.today()
        result = sorted(filters.upcoming(self._events, today), key=_sort_key)
        if limit is not None:
            result = result[:limit]
        return result

    def between(self, start, end):
        """Events from ``start`` to ``end`` inclusive, in chronological order."""
        return sorted(filters.in_range(self._events, start, end), key=_sort_key)

    def tagged(self, tag):
        return sorted(filters.with_tag(self._events, tag), key=_sort_key)

    def agenda(self, today=None, limit=None):
        """Text agenda of the upcoming events."""
        return format_agenda(self.upcoming(today=today, limit=limit))
