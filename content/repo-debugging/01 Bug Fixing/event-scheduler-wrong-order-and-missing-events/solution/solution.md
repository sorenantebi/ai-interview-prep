# Event Scheduler: Wrong Order and Missing Events - Solution

## Root causes / approach

**1. Wrong ordering: `scheduler/service.py`, `_sort_key`.**
The key used `event.date`, the raw 'D/M/YYYY' string, so sorting was lexicographic: `"10/1/2025" < "2/12/2024" < "9/1/2025"`. The day-first format makes string order meaningless (day is compared before month and year, and digits are not padded). Fix: sort on `event.day`, the parsed `datetime.date`, with the lower-cased title as tie-breaker. Because `sorted_events`, `upcoming`, `between` and `tagged` all share `_sort_key`, one change fixes all of them.

**2. Today's events missing: `scheduler/filters.py`, `upcoming`.**
The comparison was `event.day > today`, which excludes events happening today. "Upcoming" is meant to include today, so it must be `>=`. (`in_range` already uses inclusive bounds correctly.)

**3. Shared tags: `scheduler/models.py`, `Event.__init__`.**
The default argument `tags=[]` is a single list object created at function definition time, so every event built without explicit tags shares it, and `add_tag` on one mutates all. Fix: default to `None` and build a fresh list per instance; copying with `list(tags)` also stops the event from aliasing a list the caller passes in.

## How to find it
- Start with `test_sorted_events_chronological`. Print `[e.date for e in scheduler.sorted_events()]` and notice the order is alphabetical by string. Trace `sorted_events` to `_sort_key` and see it uses `.date` rather than `.day`.
- `test_upcoming_includes_today` fails with "Today" missing while the other events are right, pointing at the boundary comparison in `filters.upcoming`; `test_upcoming_excludes_past` passes, so only the boundary is wrong.
- `test_tags_are_per_event` shows a tag on an event that was never tagged. Shared state across instances points at a mutable default argument; print `first.tags is second.tags` to confirm.
