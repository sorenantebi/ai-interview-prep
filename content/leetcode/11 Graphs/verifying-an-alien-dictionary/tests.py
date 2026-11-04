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

ABC = "abcdefghijklmnopqrstuvwxyz"
REV = ABC[::-1]

cases = [
    (["hello", "leetcode"], "hlabcdefgijkmnopqrstuvwxyz", True),
    (["word", "world", "row"], "worldabcefghijkmnpqstuvxyz", False),
    (["apple", "app"], ABC, False),
    (["single"], ABC, True),
    (["abc", "abc"], ABC, True),
    (["app", "apple"], ABC, True),
    (["z", "a"], REV, True),
    (["z", "a"], ABC, False),
    (["kuvp", "q"], "ngxlkthsjuoqcpavbfdermiywz", True),
    (["a", "b", "c"], "cbadefghijklmnopqrstuvwxyz", False),
    (["abc", "abd", "abca"], ABC, False),
    (["abc", "ab"], ABC, False),
    (["ubg", "kwh"], "qcipyamwvdjtesbghlorufnkzx", True),
    (["a" * 20] * 50 + ["a" * 19 + "b"] * 50, ABC, True),
    (["a" * 20] * 50 + ["a" * 19 + "b"] * 50 + ["a" * 20], ABC, False),
]

passed = 0
total = len(cases)
for i, (words, order, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().isAlienSorted(list(words), order)
        ok = got == expected
    except Exception as e:
        ok = False
        got = f"{type(e).__name__}: {e}"
    if ok:
        passed += 1
        print(f"PASS case {i}")
    else:
        shown = words if len(words) <= 5 else f"<{len(words)} words>"
        print(f"FAIL case {i}: input=({shown}, {order!r}), expected={expected}, got={got}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
