import sys
import traceback
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


def build_list(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def serialize_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def build_tree(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def serialize_tree(root):
    if not root:
        return []
    out, queue = [], [root]
    while queue:
        node = queue.pop(0)
        if node:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)
Solution = ns["Solution"]


# Large inputs
large_chain = ["1"] + ["1", "+"] * 4999          # 9999 tokens, result 5000
large_deep = ["1"] * 5000 + ["+"] * 4999          # 9999 tokens, deep stack, result 5000

cases = [
    (["2", "1", "+", "3", "*"], 9),
    (["4", "13", "5", "/", "+"], 6),
    (["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"], 22),
    (["42"], 42),
    (["-200"], -200),
    (["3", "5", "-"], -2),
    (["-7", "2", "/"], -3),
    (["7", "-2", "/"], -3),
    (["-1", "2", "/"], 0),
    (["-6", "-3", "/"], 2),
    (["-4", "5", "*"], -20),
    (["0", "3", "/"], 0),
    (["5", "1", "2", "+", "4", "*", "+", "3", "-"], 14),
    (large_chain, 5000),
    (large_deep, 5000),
]


def short(tokens):
    if len(tokens) > 20:
        return "[" + ", ".join(repr(t) for t in tokens[:10]) + ", ...] (len=%d)" % len(tokens)
    return repr(tokens)


passed = 0
for i, (tokens, expected) in enumerate(cases, 1):
    try:
        got = Solution().evalRPN(list(tokens))
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={short(tokens)}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={short(tokens)}, expected={expected}, got=Exception: {type(e).__name__}: {e}")

print(f"{passed}/{len(cases)} passed")
if passed != len(cases):
    sys.exit(1)