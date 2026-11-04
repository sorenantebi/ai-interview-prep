---
topic: "Line Sweep"
difficulty: Medium
leetcode: https://leetcode.com/problems/corporate-flight-bookings/
---
# Corporate Flight Bookings

**Topic:** Line Sweep · **Difficulty:** Medium

## Problem

There are `n` flights labeled from `1` to `n`.

You are given an array `bookings`, where `bookings[i] = [first_i, last_i, seats_i]` is a booking that reserves `seats_i` seats on every flight from `first_i` through `last_i` (inclusive).

Return an array `answer` of length `n`, where `answer[i]` is the total number of seats reserved for flight `i + 1` (that is, `answer` is 0-indexed while flight labels are 1-indexed).

## Examples

**Example 1**
```text
Input: bookings = [[1,2,10],[2,3,20],[2,5,25]], n = 5
Output: [10,55,45,25,25]
```
Flight labels: 1, 2, 3, 4, 5. Booking 1 reserves 10 seats on flights 1-2, booking 2 reserves 20 on flights 2-3, and booking 3 reserves 25 on flights 2-5. The totals are 10, 55, 45, 25, 25.

**Example 2**
```text
Input: bookings = [[1,2,10],[2,2,15]], n = 2
Output: [10,25]
```
Flight 1 gets 10 seats; flight 2 gets 10 + 15 = 25 seats.

## Constraints

- `1 <= n <= 2 * 10^4`
- `1 <= bookings.length <= 2 * 10^4`
- `bookings[i].length == 3`
- `1 <= first_i <= last_i <= n`
- `1 <= seats_i <= 10^4`
