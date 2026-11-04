---
video: https://www.youtube.com/watch?v=qYlHrAKJfyA
topic: "Stack"
difficulty: Medium
leetcode: https://leetcode.com/problems/simplify-path/
neetcode: https://neetcode.io/problems/simplify-path
---
# Simplify Path

**Topic:** Stack · **Difficulty:** Medium

## Problem

You are given an absolute path for a Unix-style file system, which always begins with a slash `'/'`. Transform it into its simplified canonical path.

The rules of a Unix-style file system are:

- A single period `'.'` represents the current directory.
- A double period `'..'` represents the parent directory.
- Multiple consecutive slashes such as `'//'` and `'///'` are treated as a single slash `'/'`.
- Any other sequence of periods (for example `'...'` or `'....'`) is treated as a valid directory or file name.

The simplified canonical path must follow these rules:

- It starts with a single slash `'/'`.
- Directories are separated by exactly one slash `'/'`.
- It does not end with a slash `'/'`, unless it is the root directory.
- It contains no `'.'` or `'..'` components used to denote the current or parent directory.

Return the simplified canonical path.

## Examples

**Example 1**
```text
Input: path = "/home/"
Output: "/home"
```
The trailing slash is removed.

**Example 2**
```text
Input: path = "/home//foo/"
Output: "/home/foo"
```
Multiple consecutive slashes are replaced by a single one.

**Example 3**
```text
Input: path = "/home/user/Documents/../Pictures"
Output: "/home/user/Pictures"
```
`".."` moves up one level to the parent directory.

**Example 4**
```text
Input: path = "/../"
Output: "/"
```
Going up from the root directory is not possible.

**Example 5**
```text
Input: path = "/.../a/../b/c/../d/./"
Output: "/.../b/d"
```
`"..."` is a valid directory name.

## Constraints

- `1 <= path.length <= 3000`
- `path` consists of English letters, digits, period `'.'`, slash `'/'`, or `'_'`.
- `path` is a valid absolute Unix path.
