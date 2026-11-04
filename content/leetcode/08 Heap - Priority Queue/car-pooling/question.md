---
video: https://www.youtube.com/watch?v=08sn_w4LWEE
topic: "Heap - Priority Queue"
difficulty: Medium
leetcode: https://leetcode.com/problems/car-pooling/
neetcode: https://neetcode.io/problems/car-pooling
---
# Car Pooling

**Topic:** Heap - Priority Queue · **Difficulty:** Medium

## Problem

A car has `capacity` empty seats and only drives east; it never turns around. You are given `trips`, where `trips[i] = [numPassengers, from, to]` describes a group of `numPassengers` people who must be picked up at kilometer `from` and dropped off at kilometer `to`. Locations are measured in kilometers due east of the car's starting point.

At any location, passengers who are getting off leave before new passengers get on. At every point along the route, the number of passengers in the car must never exceed `capacity`.

Return `true` if all trips can be completed, or `false` otherwise.

## Examples

**Example 1**
```text
Input: trips = [[2,1,5],[3,3,7]], capacity = 4
Output: false
```
At kilometer 3 the car would hold 2 + 3 = 5 passengers, which exceeds the capacity of 4.

**Example 2**
```text
Input: trips = [[2,1,5],[3,3,7]], capacity = 5
Output: true
```
The maximum occupancy is 5 (between kilometers 3 and 5), which never exceeds the capacity of 5.

## Constraints

- `1 <= trips.length <= 1000`
- `trips[i].length == 3`
- `1 <= numPassengers_i <= 100`
- `0 <= from_i < to_i <= 1000`
- `1 <= capacity <= 10^5`
