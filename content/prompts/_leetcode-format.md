Write exactly two files in this format (no text outside the file sections):

=== FILE: question.md ===
---
topic: "{{topic}}"
difficulty: Easy | Medium | Hard
leetcode: <leetcode url or omit the line>
neetcode: <neetcode url or omit the line>
---
# <Title>

**Topic:** {{topic}} · **Difficulty:** <difficulty>

## Problem

<statement in your own words>

## Examples

**Example 1**
```text
Input: ...
Output: ...
```
(2-3 examples)

## Constraints

- ...

=== FILE: solution.md ===
---
(same frontmatter)
---
# <Title> - Solution

## Intuition

## Approach

1. ...

## Code

```python
from typing import List, Optional

class Solution:
	def methodName(self, ...) -> ...:
		...
```
(Use LeetCode's exact class and method signature; for an original problem, a LeetCode-style `class Solution`
method. 4-space indentation. Comment only the non-obvious lines. For linked lists / trees, refer to `ListNode` /
`TreeNode` without defining them. The code must be correct and optimal: the app runs your examples against it.)

## Complexity

- **Time:** `O(...)` — why
- **Space:** `O(...)` — why

## Other Approaches

- **Name:** one line — Time / Space
=== END ===
