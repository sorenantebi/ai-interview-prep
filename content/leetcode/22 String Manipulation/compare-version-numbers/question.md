---
topic: "String Manipulation"
difficulty: Medium
leetcode: https://leetcode.com/problems/compare-version-numbers/
---
# Compare Version Numbers

**Topic:** String Manipulation · **Difficulty:** Medium

## Problem

You are given two version strings, `version1` and `version2`. A version string is made up of revisions separated by dots `'.'`. The value of a revision is its integer value, ignoring any leading zeros.

Compare the two versions by comparing their revision values from left to right. If one version has fewer revisions than the other, treat each missing revision as `0`.

Return:

- `-1` if `version1 < version2`
- `1` if `version1 > version2`
- `0` otherwise

## Examples

**Example 1**
```text
Input: version1 = "1.2", version2 = "1.10"
Output: -1
```
The second revisions are `2` and `10`, and `2 < 10`, so `version1 < version2`.

**Example 2**
```text
Input: version1 = "1.01", version2 = "1.001"
Output: 0
```
Ignoring leading zeros, both `"01"` and `"001"` represent the integer `1`.

**Example 3**
```text
Input: version1 = "1.0", version2 = "1.0.0.0"
Output: 0
```
`version1` has fewer revisions, so the missing ones are treated as `0`.

## Constraints

- `1 <= version1.length, version2.length <= 500`
- `version1` and `version2` only contain digits and `'.'`.
- `version1` and `version2` are valid version numbers.
- All revisions in `version1` and `version2` can be stored in a 32-bit integer.
