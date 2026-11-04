---
video: https://www.youtube.com/watch?v=mSVAw0AUZgA
topic: "Greedy"
difficulty: Easy
leetcode: https://leetcode.com/problems/lemonade-change/
neetcode: https://neetcode.io/problems/lemonade-change
---
# Lemonade Change

**Topic:** Greedy · **Difficulty:** Easy

## Problem

A lemonade stand sells lemonade for $5 each. Customers wait in a queue and are served one at a time, in the order given by the array `bills`. Each customer buys exactly one lemonade and pays with a $5, $10, or $20 bill. You must give each customer the correct change so that the net amount they pay is $5.

You start with no money in hand.

Given an integer array `bills`, where `bills[i]` is the bill the `i`-th customer pays with, return `true` if you can give correct change to every customer, or `false` otherwise.

## Examples

**Example 1**
```text
Input: bills = [5,5,5,10,20]
Output: true
```
The first three customers pay with $5 bills, which are kept. The fourth pays $10 and receives a $5 back. The fifth pays $20 and receives a $10 and a $5 back. Everyone gets correct change.

**Example 2**
```text
Input: bills = [5,5,10,10,20]
Output: false
```
After the first four customers we hold no $5 bills and two $10 bills. The last customer needs $15 in change, which cannot be made from two $10 bills.

## Constraints

- `1 <= bills.length <= 10^5`
- `bills[i]` is either `5`, `10`, or `20`.
