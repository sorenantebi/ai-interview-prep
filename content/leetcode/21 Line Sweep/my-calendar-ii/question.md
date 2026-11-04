---
topic: "Line Sweep"
difficulty: Medium
leetcode: https://leetcode.com/problems/my-calendar-ii/
---
# My Calendar II

**Topic:** Line Sweep · **Difficulty:** Medium

## Problem

Design a calendar that accepts new events as long as no moment in time ends up covered by three or more events (a triple booking).

An event is a pair of integers `startTime` and `endTime` describing the half-open interval `[startTime, endTime)`, i.e. all real numbers `x` with `startTime <= x < endTime`. Two events overlap if they share at least one such moment.

Implement the `MyCalendarTwo` class:

- `MyCalendarTwo()` creates an empty calendar.
- `boolean book(int startTime, int endTime)` adds the event and returns `true` if doing so does not cause a triple booking. Otherwise it returns `false` and the event is not added.

## Examples

**Example 1**
```text
Input
["MyCalendarTwo", "book", "book", "book", "book", "book", "book"]
[[], [10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]]
Output
[null, true, true, true, false, true, true]
```

Explanation:
- `book(10, 20)` returns `true`: the calendar is empty.
- `book(50, 60)` returns `true`: no overlap with `[10, 20)`.
- `book(10, 40)` returns `true`: it double books `[10, 20)`, which is allowed.
- `book(5, 15)` returns `false`: `[10, 15)` would be covered by three events.
- `book(5, 10)` returns `true`: it does not touch time 10, which is already double booked.
- `book(25, 55)` returns `true`: `[25, 40)` is double booked with the third event, `[40, 50)` is single booked, and `[50, 55)` is double booked with the second event.

## Constraints

- `0 <= startTime < endTime <= 10^9`
- At most `1000` calls will be made to `book`.
