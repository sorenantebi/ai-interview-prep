import sys
import time
import random
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
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def list_to_array(head, limit=1000000):
    out = []
    seen = 0
    while head is not None:
        out.append(head.val)
        head = head.next
        seen += 1
        if seen > limit:
            raise RuntimeError("cycle or overly long list detected")
    return out


def build_tree(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    qi = 0
    while qi < len(queue) and i < len(values):
        node = queue[qi]
        qi += 1
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if root is None:
        return []
    out = []
    queue = [root]
    qi = 0
    while qi < len(queue):
        node = queue[qi]
        qi += 1
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def run(lists_values):
    lists = [build_list(v) for v in lists_values]
    result = ns["Solution"]().mergeKLists(lists)
    return list_to_array(result)


random.seed(12345)

big_lists = []
for _ in range(100):
    big_lists.append(sorted(random.randint(-10000, 10000) for _ in range(100)))

many_singletons = [[random.randint(-10000, 10000)] for _ in range(10000)]

long_single = [sorted(random.randint(-10000, 10000) for _ in range(500))]

cases = [
    [[1, 4, 5], [1, 3, 4], [2, 6]],
    [],
    [[]],
    [[], [], []],
    [[5]],
    [[], [1], []],
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    [[-5, -3, -1], [-4, -2, 0], [-10, 10]],
    [[2, 2, 2], [2, 2], [2]],
    [[7, 8, 9], [1, 2, 3], [4, 5, 6], [0]],
    big_lists,
    many_singletons,
    long_single,
]

passed = 0
total = len(cases)
for idx, case in enumerate(cases, 1):
    expected = sorted(x for lst in case for x in lst)
    desc = repr(case) if len(repr(case)) <= 200 else "<%d lists, %d nodes>" % (len(case), len(expected))
    try:
        start = time.time()
        got = run(case)
        elapsed = time.time() - start
        if got == expected and elapsed < 10:
            print("PASS case %d" % idx)
            passed += 1
        elif got == expected:
            print("FAIL case %d: input=%s, too slow (%.2fs)" % (idx, desc, elapsed))
        else:
            exp_s = repr(expected) if len(repr(expected)) <= 200 else "<%d values>" % len(expected)
            got_s = repr(got) if len(repr(got)) <= 200 else "<%d values>" % len(got)
            print("FAIL case %d: input=%s, expected=%s, got=%s" % (idx, desc, exp_s, got_s))
    except Exception as e:
        print("FAIL case %d: input=%s, error=%s: %s" % (idx, desc, type(e).__name__, e))

print("%d/%d passed" % (passed, total))
if passed != total:
    sys.exit(1)
