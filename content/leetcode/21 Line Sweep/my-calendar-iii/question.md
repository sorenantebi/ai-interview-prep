---
topic: "Line Sweep"
difficulty: Hard
leetcode: https://leetcode.com/problems/my-calendar-iii/
---
# My Calendar III

**Topic:** Line Sweep · **Difficulty:** Hard

## Problem

A **k-booking** happens when `k` events share some non-empty intersection, meaning there is a time that is common to all `k` events.

Events are half-open intervals `[startTime, endTime)`. After each new event is added, you must report the largest `k` such that a k-booking exists among all events booked so far.

Implement the `MyCalendarThree` class:

- `MyCalendarThree()` Initializes the object.
- `int book(int startTime, int endTime)` Adds the event `[startTime, endTime)` to the calendar and returns the largest integer `k` such that there exists a k-booking in the calendar.

## Examples

**Example 1**
```text
Input
["MyCalendarThree", "book", "book", "book", "book", "book", "book"]
[[], [10, 20], [50, 60], [10, 40], [5, 15], [5, 10], [25, 55]]
Output
[null, 1, 1, 2, 3, 3, 3]
```

Explanation:
```text
MyCalendarThree myCalendarThree = new MyCalendarThree();
myCalendarThree.book(10, 20); // return 1
myCalendarThree.book(50, 60); // return 1
myCalendarThree.book(10, 40); // return 2
myCalendarThree.book(5, 15);  // return 3
myCalendarThree.book(5, 10);  // return 3
myCalendarThree.book(25, 55); // return 3
```

## Constraints

- `0 <= startTime < endTime <= 10^9`
- At most `400` calls will be made to `book`.
