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


def build_list(vals):
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
    return head


def list_to_array(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def is_valid(s, a, b, c, expected_len):
    if not isinstance(s, str):
        return False
    if len(s) != expected_len:
        return False
    if any(ch not in "abc" for ch in s):
        return False
    if "aaa" in s or "bbb" in s or "ccc" in s:
        return False
    return s.count("a") <= a and s.count("b") <= b and s.count("c") <= c


# (a, b, c, expected maximum length)
CASES = [
    (1, 1, 7, 8),
    (7, 1, 0, 5),
    (0, 0, 1, 1),
    (1, 0, 0, 1),
    (2, 2, 2, 6),
    (0, 0, 5, 2),
    (0, 5, 5, 10),
    (100, 100, 100, 300),
    (100, 0, 0, 2),
    (100, 1, 0, 5),
    (100, 100, 0, 200),
    (3, 0, 1, 4),
    (1, 1, 1, 3),
    (50, 1, 1, 8),
]

passed = 0
total = len(CASES)
for i, (a, b, c, exp_len) in enumerate(CASES, 1):
    try:
        got = ns["Solution"]().longestDiverseString(a, b, c)
        if is_valid(got, a, b, c, exp_len):
            print(f"PASS case {i}")
            passed += 1
        else:
            shown = got if not isinstance(got, str) or len(got) <= 60 else got[:60] + "..."
            print(f"FAIL case {i}: input=({a}, {b}, {c}), expected=valid happy string of length {exp_len}, got={shown!r} (len {len(got) if hasattr(got, '__len__') else '?'})")
    except Exception as e:
        print(f"FAIL case {i}: input=({a}, {b}, {c}), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)