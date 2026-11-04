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

cases = [
    ("RD", "Radiant"),
    ("RDD", "Dire"),
    ("R", "Radiant"),
    ("D", "Dire"),
    ("DR", "Dire"),
    ("RRDD", "Radiant"),
    ("DDRR", "Dire"),
    ("RDRDRD", "Radiant"),
    ("DRDRDR", "Dire"),
    ("RRRDD", "Radiant"),
    ("DDRRR", "Dire"),
    ("RDDR", "Radiant"),
    ("R" * 5000 + "D" * 5000, "Radiant"),
    ("DR" * 5000, "Dire"),
]

passed = 0
total = len(cases)
for i, (senate, expected) in enumerate(cases, 1):
    shown = senate if len(senate) <= 40 else senate[:20] + "..." + f"(len {len(senate)})"
    try:
        got = ns["Solution"]().predictPartyVictory(senate)
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={shown!r}, expected={expected!r}, got={got!r}")
    except Exception as e:
        print(f"FAIL case {i}: input={shown!r}, expected={expected!r}, got=error: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
