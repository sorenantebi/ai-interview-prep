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
    (4, 4),
    (25, 1389537),
    (0, 0),
    (1, 1),
    (2, 1),
    (3, 2),
    (5, 7),
    (10, 149),
    (20, 66012),
    (30, 29249425),
    (36, 1132436852),
    (37, 2082876103),
]

passed = 0
for i, (n, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().tribonacci(n)
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={n}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={n}, expected={expected}, got=exception {type(e).__name__}: {e}")

# Extra case: recurrence holds for every n in the valid range (checked in one pass)
i = len(cases) + 1
total = len(cases) + 1
try:
    sol = ns["Solution"]()
    vals = [sol.tribonacci(n) for n in range(38)]
    ok = vals[:3] == [0, 1, 1] and all(
        vals[k] == vals[k - 1] + vals[k - 2] + vals[k - 3] for k in range(3, 38)
    )
    if ok:
        print(f"PASS case {i}")
        passed += 1
    else:
        print(f"FAIL case {i}: input=range(38), expected=sequence satisfying recurrence, got={vals}")
except Exception as e:
    print(f"FAIL case {i}: input=range(38), expected=valid sequence, got=exception {type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)