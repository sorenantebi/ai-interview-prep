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
Solution = ns["Solution"]


def is_valid(t):
    bal = 0
    for c in t:
        if c == '(':
            bal += 1
        elif c == ')':
            bal -= 1
            if bal < 0:
                return False
    return bal == 0


def only_parens_removed(s, t):
    j = 0
    for c in s:
        if j < len(t) and t[j] == c:
            j += 1
        elif c not in "()":
            return False
    return j == len(t)


def check(s, expected, got):
    if not isinstance(got, str):
        return False
    return (is_valid(got) and only_parens_removed(s, got)
            and len(got) == len(expected))


cases = [
    ("lee(t(c)o)de)", "lee(t(c)o)de"),
    ("a)b(c)d", "ab(c)d"),
    ("))((", ""),
    ("abc", "abc"),
    ("(", ""),
    (")", ""),
    ("()", "()"),
    ("(a(b(c)d)", "a(b(c)d)"),
    (")(", ""),
    ("((a))", "((a))"),
    ("a(b)c)d(e", "a(b)cde"),
    ("(" * 50000 + ")" * 50000, "(" * 50000 + ")" * 50000),
    (")" * 50000 + "(" * 50000, ""),
    ("(" * 30000 + "a" + ")" * 40000, "(" * 30000 + "a" + ")" * 30000),
]

passed = 0
total = len(cases)
for i, (s, expected) in enumerate(cases, 1):
    disp_s = s if len(s) <= 60 else s[:20] + "...(len %d)" % len(s)
    disp_e = expected if len(expected) <= 60 else "(len %d)" % len(expected)
    try:
        got = Solution().minRemoveToMakeValid(s)
        if check(s, expected, got):
            print(f"PASS case {i}")
            passed += 1
        else:
            disp_g = got if not isinstance(got, str) or len(got) <= 60 else "(len %d)" % len(got)
            print(f"FAIL case {i}: input={disp_s!r}, expected={disp_e!r} (or any equally valid), got={disp_g!r}")
    except Exception as e:
        print(f"FAIL case {i}: input={disp_s!r}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)