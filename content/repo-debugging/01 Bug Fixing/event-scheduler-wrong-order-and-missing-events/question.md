---
difficulty: Medium
kind: bug-fix
---
# Event Scheduler: Wrong Order and Missing Events

**Kind:** Bug fix · **Difficulty:** Medium

## Scenario
The `scheduler` package keeps a list of events (title, date, category, tags) and is used by an internal team calendar to show agendas and "what's coming up". Since the last release, users report that agendas are in a strange order around month and year boundaries, that events scheduled for today vanish from the "upcoming" view, and that tagging one event sometimes seems to tag others too.

## Your tasks
1. Users report that events are listed in the wrong order, for example a 10 January event appears before a 2 December event from the previous year. Find and fix the cause (the failing tests show the symptoms).
2. Users report that an event happening today is not shown in the "upcoming" list. Find and fix the cause.
3. Users report that adding a tag to one event makes the tag show up on unrelated events. Find and fix the cause.
4. Make sure all visible tests pass and that you have not changed the public behaviour of the other functions.

## Notes
- Dates are stored as `'D/M/YYYY'` strings (day first, zero padding optional); `scheduler/dateutil.py` has the helpers for them.
- The main entry point is `scheduler.service.Scheduler`; the pure filtering helpers live in `scheduler/filters.py`.
- Each of the three problems is in a different place, so do not assume one fix will cover everything.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
