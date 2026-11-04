---
video: https://www.youtube.com/watch?v=2VLwjvODQbA
topic: "Intervals"
difficulty: Hard
leetcode: https://leetcode.com/problems/meeting-rooms-iii/
neetcode: https://neetcode.io/problems/meeting-rooms-iii
---
# Meeting Rooms III

**Topic:** Intervals · **Difficulty:** Hard

## Problem

You are given an integer `n`. There are `n` rooms numbered from `0` to `n - 1`.

You are also given a 2D integer array `meetings` where `meetings[i] = [start_i, end_i]` means a meeting will be held during the half-closed time interval `[start_i, end_i)`. All values of `start_i` are unique.

Meetings are assigned to rooms as follows:

- Each meeting takes place in the unused room with the lowest number.
- If no room is available, the meeting is delayed until a room becomes free. A delayed meeting keeps the same duration as the original meeting.
- When a room becomes free, meetings with an earlier original start time get the room first.

Return the number of the room that held the most meetings. If several rooms tie, return the one with the lowest number.

A half-closed interval `[a, b)` includes `a` but not `b`.

## Examples

**Example 1**
```text
Input: n = 2, meetings = [[0,10],[1,5],[2,7],[3,4]]
Output: 0
```
Room 0 takes the first meeting at time 0 and room 1 takes the second at time 1. The third and fourth meetings are delayed. At time 5 room 1 frees up and takes the third meeting for `[5,10)`. At time 10 both rooms free up and the fourth meeting goes to room 0 for `[10,11)`. Both rooms held 2 meetings, so the answer is 0.

**Example 2**
```text
Input: n = 3, meetings = [[1,20],[2,10],[3,5],[4,9],[6,8]]
Output: 1
```
Room 0 holds 1 meeting, while rooms 1 and 2 each hold 2 meetings. The lowest-numbered room among those is 1.

## Constraints

- `1 <= n <= 100`
- `1 <= meetings.length <= 10^5`
- `meetings[i].length == 2`
- `0 <= start_i < end_i <= 5 * 10^5`
- All the values of `start_i` are unique.
