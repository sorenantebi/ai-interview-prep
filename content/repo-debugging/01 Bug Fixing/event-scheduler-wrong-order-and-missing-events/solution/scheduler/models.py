"""Data model for calendar events."""

from scheduler.dateutil import parse_date


class Event:
    """A single calendar entry.

    ``date`` is kept exactly as entered ('D/M/YYYY'); use :attr:`day` to get
    a real ``datetime.date``.
    """

    def __init__(self, title, date, category="general", tags=None):
        self.title = title
        self.date = date
        self.category = category
        self.tags = list(tags) if tags else []

    @property
    def day(self):
        """The event date as a ``datetime.date``."""
        return parse_date(self.date)

    def add_tag(self, tag):
        """Attach a tag to this event if it is not already present."""
        if tag not in self.tags:
            self.tags.append(tag)

    def has_tag(self, tag):
        return tag in self.tags

    def __repr__(self):
        return f"Event({self.title!r}, {self.date!r}, category={self.category!r})"
