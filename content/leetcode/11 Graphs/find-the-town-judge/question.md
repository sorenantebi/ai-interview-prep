---
video: https://www.youtube.com/watch?v=QiGaxdUINJ8
topic: "Graphs"
difficulty: Easy
leetcode: https://leetcode.com/problems/find-the-town-judge/
neetcode: https://neetcode.io/problems/find-the-town-judge
---
# Find the Town Judge

**Topic:** Graphs · **Difficulty:** Easy

## Problem

A town has `n` people labeled from `1` to `n`. Rumor has it that one of them is secretly the town judge.

If the town judge exists, then:

1. The town judge trusts nobody.
2. Everybody else (everyone except the judge) trusts the town judge.
3. Exactly one person satisfies both properties 1 and 2.

You are given an array `trust` where `trust[i] = [ai, bi]` means the person labeled `ai` trusts the person labeled `bi`. Any trust relationship not listed in `trust` does not exist.

Return the label of the town judge if the judge exists and can be identified, otherwise return `-1`.

## Examples

**Example 1**
```text
Input: n = 2, trust = [[1,2]]
Output: 2
```

**Example 2**
```text
Input: n = 3, trust = [[1,3],[2,3]]
Output: 3
```

**Example 3**
```text
Input: n = 3, trust = [[1,3],[2,3],[3,1]]
Output: -1
```

## Constraints

- `1 <= n <= 1000`
- `0 <= trust.length <= 10^4`
- `trust[i].length == 2`
- All the pairs of `trust` are unique.
- `ai != bi`
- `1 <= ai, bi <= n`
