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
    ([2, 0, 2, 1, 1, 0], [0, 0, 1, 1, 2, 2]),
    ([2, 0, 1], [0, 1, 2]),
    ([0], [0]),
    ([1], [1]),
    ([2], [2]),
    ([1, 0], [0, 1]),
    ([2, 1], [1, 2]),
    ([2, 0], [0, 2]),
    ([1, 1, 1, 1], [1, 1, 1, 1]),
    ([0, 0, 1, 1, 2, 2], [0, 0, 1, 1, 2, 2]),
    ([2, 2, 1, 1, 0, 0], [0, 0, 1, 1, 2, 2]),
    ([2, 1, 0] * 100, [0] * 100 + [1] * 100 + [2] * 100),
    ([2] * 150 + [0] * 150, [0] * 150 + [2] * 150),
]

passed = 0
total = len(cases)
for n, (inp, expected) in enumerate(cases, 1):
    arg = list(inp)
    shown = inp if len(inp) <= 20 else f"<list of {len(inp)}>"
    shown_exp = expected if len(expected) <= 20 else f"<list of {len(expected)}>"
    try:
        sol = ns["Solution"]()
        sol.sortColors(arg)
        if arg == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            got = arg if len(arg) <= 20 else f"<list of {len(arg)}>"
            print(f"FAIL case {n}: input={shown}, expected={shown_exp}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input={shown}, expected={shown_exp}, got=error: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)