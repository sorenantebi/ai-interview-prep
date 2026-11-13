import sys
from typing import List, Optional, Dict


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

cases = [
    ("sadbutsad", "sad", 0),
    ("leetcode", "leeto", -1),
    ("a", "a", 0),
    ("a", "b", -1),
    ("abc", "abcd", -1),
    ("mississippi", "issip", 4),
    ("mississippi", "issipi", -1),
    ("aabaaabaaac", "aabaaac", 4),
    ("hello", "ll", 2),
    ("abc", "c", 2),
    ("abcabcabd", "abcabd", 3),
    ("a" * 9999 + "b", "a" * 5000 + "b", 4999),
    ("a" * 10000, "a" * 5000 + "b", -1),
]


def short(s):
    return s if len(s) <= 40 else s[:20] + "...(len %d)" % len(s)


passed = 0
for n, (h, nd, exp) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().strStr(h, nd)
        if got == exp:
            passed += 1
            print(f"PASS case {n}")
        else:
            print(f"FAIL case {n}: input=({short(h)!r}, {short(nd)!r}), expected={exp}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input=({short(h)!r}, {short(nd)!r}), error={type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)