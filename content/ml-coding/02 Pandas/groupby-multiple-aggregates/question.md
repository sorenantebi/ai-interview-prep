---
topic: "Pandas"
difficulty: Medium
---
# Group By with Several Aggregates

**Topic:** Pandas · **Difficulty:** Medium

## Problem

You get a DataFrame `df` of game results with columns `team`, `player` and `points`. A player can appear in several rows.

Return one row per team, sorted by team name, with these columns in this order:

- `team`
- `players`: the number of distinct players of that team
- `total`: the sum of `points`
- `mean`: the mean of `points` over the team's rows
- `best`: the highest `points` value

Use a default `0..n-1` index.

## Examples

**Example 1**
```text
Input: df = {"team": ["red", "blue", "red", "red"], "player": ["al", "bo", "cy", "al"], "points": [10, 7, 4, 6]}
Output: {"team":["blue","red"],"players":[1,2],"total":[7,20],"mean":[7.00000,6.66667],"best":[7,10]}
Explanation: red has two distinct players (al twice) and points 10, 4 and 6.
```

**Example 2**
```text
Input: df = {"team": ["x"], "player": ["p"], "points": [3]}
Output: {"team":["x"],"players":[1],"total":[3],"mean":[3.00000],"best":[3]}
```

## Constraints

- `0 <= len(df) <= 10^5`
- `points` has no missing values
