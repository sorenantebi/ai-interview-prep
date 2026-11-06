"""Plain-text rendering of event lists."""

from scheduler.dateutil import format_date


def format_agenda(events):
    """Render events as one line each: 'D/M/YYYY - Title (category)'."""
    if not events:
        return "No events."
    lines = [
        f"{format_date(event.day)} - {event.title} ({event.category})"
        for event in events
    ]
    return "\n".join(lines)
