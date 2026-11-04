---
topic: "Line Sweep"
difficulty: Easy
leetcode: https://leetcode.com/problems/maximum-population-year/
---
# Maximum Population Year

**Topic:** Line Sweep · **Difficulty:** Easy

## Problem

You are given a 2D integer array `logs` where each `logs[i] = [birth_i, death_i]` gives the birth year and death year of the `i`-th person.

The population of a year `x` is the number of people alive during that year. The `i`-th person counts toward year `x` if `x` lies in the inclusive range `[birth_i, death_i - 1]`. In other words, a person is not counted in the year they die.

Return the earliest year that has the maximum population.

## Examples

**Example 1**
```text
Input: logs = [[1993,1999],[2000,2010]]
Output: 1993
Explanation: The maximum population is 1, and 1993 is the earliest year with this population.
```

**Example 2**
```text
Input: logs = [[1950,1961],[1960,1971],[1970,1981]]
Output: 1960
Explanation: The maximum population is 2, reached in both 1960 and 1970. The earlier year is 1960.
```

## Constraints

- `1 <= logs.length <= 100`
- `1950 <= birth_i < death_i <= 2050`
