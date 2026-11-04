---
topic: "Stack"
difficulty: Medium
leetcode: https://leetcode.com/problems/simplify-path/
neetcode: https://neetcode.io/problems/simplify-path
---
# Simplify Path - Solution

## Intuition

Directory names behave like a stack: entering a directory pushes it, and `..` pops the most recent one. Empty segments (from repeated slashes) and `.` do nothing.

## Approach

1. Split the path on `'/'` to get its components.
2. For each component:
   - If it is empty or `'.'`, skip it.
   - If it is `'..'`, pop from the stack if it is non-empty.
   - Otherwise, push it onto the stack.
3. Join the stack with `'/'` and prepend a leading `'/'`. An empty stack yields `'/'`.

## Code

```python
class Solution:
    def simplifyPath(self, path: str) -> str:

        stack = []

        for i in path.split("/"):
            #  if i == "/" or i == '//', it becomes '' (empty string)

            if i == "..":
                if stack:
                    stack.pop()
            elif i == "." or i == '':
                # skip "." or an empty string
                continue
            else:
                stack.append(i)

        res = "/" + "/".join(stack)
        return res
```

## Complexity

- **Time:** `O(n)` — each character is processed once by the split, and each component is pushed and popped at most once.
- **Space:** `O(n)` — the stack and the split components hold at most the characters of the input.

## Other Approaches

- **Manual character scan:** build each component character by character instead of using `split`, with the same stack logic — Time `O(n)` / Space `O(n)`

## C++

```cpp
/*
    Given an absolute path to a file or directory in a Unix-style file system,
    convert it to the simplified canonical path.

    In a Unix-style file system, a period '.' refers to the current directory.
    A double period '..' refers to the directory up a level.
    Any multiple consecutive slashes (i.e. '//') are treated as a single slash '/'.
    For this problem, any other format of periods such as '...' are treated as file/directory names.

    The canonical path should have the following format:
    - The path starts with a single slash '/'.
    - Any two directories are separated by a single slash '/'.
    - The path does not end with a trailing '/'.
    - The path only contains the directories on the path from the root directory to the target file or directory (i.e., no period '.' or double period '..')

    Return the simplified canonical path.

    Time: O(n)
    Space: O(n)
*/

class Solution {
public:
    string simplifyPath(string path) {
        stringstream ss(path);
        string dir;
        stack<string> stk;

        while (getline(ss, dir, '/')) {
            if (dir.empty() || dir == ".") {
                continue;
            }
            else if (dir == "..") {
                if (!stk.empty())
                    stk.pop();
            }
            else {
                stk.push(dir);
            }
        }

        string res = "";
        while (!stk.empty()) {
            res = "/" + stk.top() + res;
            stk.pop();
        }
        return res.empty()? "/" : res;
    }
};
```
