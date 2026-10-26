---
topic: "Pandas"
difficulty: Medium
---
# Deduplicate, Keeping the Latest Row

**Topic:** Pandas · **Difficulty:** Medium

## Problem

You get a DataFrame `df` of profile updates with columns `user_id`, `updated_at` (an ISO string `"YYYY-MM-DD HH:MM:SS"`) and `email`. A user can have many rows, in any order.

Return one row per user: the row with the latest `updated_at`. If a user has several rows with that same latest time, keep the one that appears last in `df`. Sort the result by `user_id`, keep the columns as they are (`updated_at` stays a string) and use a default `0..n-1` index.

## Examples

**Example 1**
```text
Input: df = {"user_id": [1, 2, 1], "updated_at": ["2024-03-01 10:00:00", "2024-01-05 09:00:00", "2024-02-01 08:00:00"], "email": ["a@new", "b@x", "a@old"]}
Output: {"user_id":[1,2],"updated_at":["2024-03-01 10:00:00","2024-01-05 09:00:00"],"email":["a@new","b@x"]}
```

**Example 2**
```text
Input: df = {"user_id": [7, 7], "updated_at": ["2024-01-01 00:00:00", "2024-01-01 00:00:00"], "email": ["first", "second"]}
Output: {"user_id":[7],"updated_at":["2024-01-01 00:00:00"],"email":["second"]}
Explanation: both rows have the same time, so the later row wins.
```

## Constraints

- `0 <= len(df) <= 10^5`
