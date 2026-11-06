from datetime import date

from scheduler.models import Event
from scheduler.service import Scheduler


def make_scheduler(*pairs):
    scheduler = Scheduler()
    for title, day in pairs:
        scheduler.add(Event(title, day))
    return scheduler


def test_add_returns_event():
    scheduler = Scheduler()
    event = Event("Standup", "3/3/2025")
    assert scheduler.add(event) is event
    assert len(scheduler) == 1


def test_add_rejects_invalid_date():
    scheduler = Scheduler()
    try:
        scheduler.add(Event("Broken", "31/2/2025"))
    except ValueError:
        return
    assert False, "expected ValueError"


def test_sorted_events_chronological():
    scheduler = make_scheduler(
        ("Late", "10/1/2025"),
        ("Early", "2/12/2024"),
        ("Middle", "9/1/2025"),
    )
    titles = [event.title for event in scheduler.sorted_events()]
    assert titles == ["Early", "Middle", "Late"], titles


def test_sorted_events_day_is_numeric():
    scheduler = make_scheduler(
        ("C", "10/2/2025"),
        ("A", "1/2/2025"),
        ("B", "9/2/2025"),
    )
    titles = [event.title for event in scheduler.sorted_events()]
    assert titles == ["A", "B", "C"], titles


def test_sorted_events_reverse():
    scheduler = make_scheduler(("A", "1/2/2025"), ("B", "10/2/2025"))
    titles = [event.title for event in scheduler.sorted_events(reverse=True)]
    assert titles == ["B", "A"], titles


def test_remove_by_title():
    scheduler = make_scheduler(("A", "1/2/2025"), ("B", "2/2/2025"))
    assert scheduler.remove("A") == 1
    assert [event.title for event in scheduler.sorted_events()] == ["B"]


def test_upcoming_includes_today():
    scheduler = make_scheduler(
        ("Past", "9/3/2025"),
        ("Today", "10/3/2025"),
        ("Tomorrow", "11/3/2025"),
        ("Later", "2/4/2025"),
    )
    titles = [event.title for event in scheduler.upcoming(today=date(2025, 3, 10))]
    assert titles == ["Today", "Tomorrow", "Later"], titles


def test_upcoming_limit():
    scheduler = make_scheduler(
        ("Today", "10/3/2025"),
        ("Tomorrow", "11/3/2025"),
        ("Later", "2/4/2025"),
    )
    result = scheduler.upcoming(today=date(2025, 3, 10), limit=2)
    assert [event.title for event in result] == ["Today", "Tomorrow"]
