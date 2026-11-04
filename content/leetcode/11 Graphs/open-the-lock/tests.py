import sys
from collections import deque
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


ns = {
    "ListNode": ListNode,
    "TreeNode": TreeNode,
    "List": List,
    "Optional": Optional,
    "Dict": Dict,
    "deque": deque,
}
exec(open("attempt.py").read(), ns)

cases = [
    # 1-3: examples
    (["0201", "0101", "0102", "1212", "2002"], "0202", 6),
    (["8888"], "0009", 1),
    (["8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"], "8888", -1),
    # 4: start is a dead end
    (["0000"], "5555", -1),
    # 5: target is the start
    (["1111"], "0000", 0),
    # 6: simple
    (["2222"], "1111", 4),
    # 7: farthest state
    (["9999"], "5555", 20),
    # 8: wraparound on every wheel
    (["0001"], "9999", 4),
    # 9: wraparound single move with irrelevant dead ends
    (["0100"], "0900", 1),
    # 10: all neighbours of the start blocked
    (["1000", "9000", "0100", "0900", "0010", "0090", "0001", "0009"], "5555", -1),
    # 11: detour around a dead end
    (["0001"], "0002", 4),
    # 12: large dead end list that does not block shortest paths
    ([f"{i:04d}" for i in range(7000, 7500)], "5555", 20),
]

passed = 0
total = len(cases)
for n, (dead, target, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().openLock(list(dead), target)
        if got == expected:
            passed += 1
            print(f"PASS case {n}")
        else:
            print(f"FAIL case {n}: input=deadends={dead[:10]}{'...' if len(dead) > 10 else ''}, target={target!r}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {n}: input=deadends={dead[:10]}, target={target!r}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
