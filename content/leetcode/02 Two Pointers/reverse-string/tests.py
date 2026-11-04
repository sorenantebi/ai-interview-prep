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


def build_list(arr):
    head = None
    for v in reversed(arr):
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


def short(x):
    r = repr(x)
    return r if len(r) <= 120 else r[:117] + "..."


big = [chr(33 + i % 90) for i in range(100000)]
big_odd = [chr(33 + (i * 7) % 90) for i in range(99999)]

cases = [
    list("hello"),
    list("Hannah"),
    ["a"],
    ["a", "b"],
    ["a", "b", "c"],
    list("abcd"),
    ["x"] * 7,
    list("a b,c!"),
    list("12321"),
    ["A", "a", "A", "a", "A", "a"],
    list("~ }|{ 0"),
    big,
    big_odd,
]
expected = [
    ["o", "l", "l", "e", "h"],
    ["h", "a", "n", "n", "a", "H"],
    ["a"],
    ["b", "a"],
    ["c", "b", "a"],
    ["d", "c", "b", "a"],
    ["x"] * 7,
    ["!", "c", ",", "b", " ", "a"],
    list("12321"),
    ["a", "A", "a", "A", "a", "A"],
    ["0", " ", "{", "|", "}", " ", "~"],
    big[::-1],
    big_odd[::-1],
]

passed = 0
total = len(cases)
for i, (inp, exp) in enumerate(zip(cases, expected), 1):
    arg = list(inp)
    try:
        ns["Solution"]().reverseString(arg)
        if arg == exp:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={short(inp)}, expected={short(exp)}, got={short(arg)}")
    except Exception as e:
        print(f"FAIL case {i}: input={short(inp)}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)