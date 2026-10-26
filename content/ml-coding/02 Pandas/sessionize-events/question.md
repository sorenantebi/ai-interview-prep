---
topic: "Pandas"
difficulty: Hard
---
# Sessionize Events

**Topic:** Pandas · **Difficulty:** Hard

## Problem

You get a DataFrame `df` of click events with columns `user` and `ts` (an ISO string `"YYYY-MM-DD HH:MM:SS"`), in any order, and an integer `gap_minutes`.

Split each user's events into sessions. Order the events by `user`, then by time (events with the same user and time keep their order from `df`). A user's first event starts a session, and so does any event that comes **more than** `gap_minutes` minutes after that user's previous event; a gap of exactly `gap_minutes` stays in the same session.

Return the events in that order with columns `user`, `ts` (the original strings) and `session`, an integer session id. Ids start at 1 and count up across the whole result in that order: the first session of the first user is 1, the next session (of the same or the next user) is 2, and so on. Use a default `0..n-1` index.

## Examples

**Example 1**
```text
Input: df = {"user": ["u1", "u1", "u2", "u1"], "ts": ["2024-01-01 10:00:00", "2024-01-01 10:20:00", "2024-01-01 09:00:00", "2024-01-01 11:00:00"]}, gap_minutes = 30
Output: {"user":["u1","u1","u1","u2"],"ts":["2024-01-01 10:00:00","2024-01-01 10:20:00","2024-01-01 11:00:00","2024-01-01 09:00:00"],"session":[1,1,2,3]}
Explanation: u1's 11:00 event is 40 minutes after 10:20, so it starts u1's second session (id 2); u2 comes next as session 3.
```

**Example 2**
```text
Input: df = {"user": ["a", "a"], "ts": ["2024-01-01 00:30:00", "2024-01-01 00:00:00"]}, gap_minutes = 30
Output: {"user":["a","a"],"ts":["2024-01-01 00:00:00","2024-01-01 00:30:00"],"session":[1,1]}
Explanation: the gap is exactly 30 minutes, so both events share one session.
```

## Constraints

- `0 <= len(df) <= 10^5`
- `1 <= gap_minutes <= 10^4`
