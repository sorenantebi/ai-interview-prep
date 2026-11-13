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
    ("1.2", "1.10", -1),
    ("1.01", "1.001", 0),
    ("1.0", "1.0.0.0", 0),
    ("0.1", "1.1", -1),
    ("1.0.1", "1", 1),
    ("7.5.2.4", "7.5.3", -1),
    ("1", "1", 0),
    ("0", "0.0.0", 0),
    ("1.0.0.0.1", "1", 1),
    ("2147483647", "2147483646", 1),
    ("00001.0002", "1.2", 0),
    ("10.0", "9.99", 1),
    ("1.0", "1.0.0.0.0.1", -1),
    (".".join(["1"] * 250), ".".join(["1"] * 249 + ["2"]), -1),
]


def main():
    passed = 0
    total = len(cases)
    for n, (v1, v2, expected) in enumerate(cases, 1):
        try:
            sol = ns["Solution"]()
            got = sol.compareVersion(v1, v2)
            if got == expected and not isinstance(got, bool):
                print(f"PASS case {n}")
                passed += 1
            else:
                s1 = v1 if len(v1) < 60 else v1[:57] + "..."
                s2 = v2 if len(v2) < 60 else v2[:57] + "..."
                print(f"FAIL case {n}: input=({s1!r}, {s2!r}), expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {n}: input=({v1[:60]!r}, {v2[:60]!r}), error={type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()