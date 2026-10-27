import random
import sys
from typing import Dict, List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Node:
    def __init__(self, x: int, next: "Node" = None, random: "Node" = None):
        self.val = int(x)
        self.next = next
        self.random = random


def build(spec):
    """Build a list from [[val, random_index], ...]; returns (head, nodes)."""
    nodes = [Node(v) for v, _ in spec]
    for i, (_, r) in enumerate(spec):
        if i + 1 < len(nodes):
            nodes[i].next = nodes[i + 1]
        if r is not None:
            nodes[i].random = nodes[r]
    return (nodes[0] if nodes else None), nodes


def collect(head, limit):
    nodes = []
    cur = head
    while cur is not None:
        nodes.append(cur)
        if len(nodes) > limit:
            raise ValueError("copy list is longer than expected (cycle or extra nodes)")
        cur = cur.next
    return nodes


def serialize(head, limit=5000):
    nodes = collect(head, limit)
    index = {id(n): i for i, n in enumerate(nodes)}
    out = []
    for n in nodes:
        if n.random is None:
            out.append([n.val, None])
        else:
            if id(n.random) not in index:
                raise ValueError("random pointer points outside the returned list")
            out.append([n.val, index[id(n.random)]])
    return out, nodes


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "Node": Node,
      "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)


def run(spec):
    head, orig_nodes = build(spec)
    orig_ids = {id(n) for n in orig_nodes}
    res = ns["Solution"]().copyRandomList(head)
    got, copy_nodes = serialize(res, len(spec) + 1)
    if any(id(n) in orig_ids for n in copy_nodes):
        raise ValueError("copy shares nodes with the original list")
    after, _ = serialize(head)
    if after != [list(p) for p in spec]:
        raise ValueError("original list was modified")
    return got


rng = random.Random(12345)
big_random = [[rng.randint(-10000, 10000), rng.choice([None] + list(range(1000)))]
              for _ in range(1000)]
big_null = [[i - 500, None] for i in range(1000)]
big_self = [[i, i] for i in range(1000)]

cases = [
    [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]],
    [[1, 1], [2, 1]],
    [[3, None], [3, 0], [3, None]],
    [],
    [[5, None]],
    [[5, 0]],
    [[-10000, 2], [0, 0], [10000, None]],
    [[1, 3], [2, 3], [3, 3], [4, 3]],
    [[1, 0], [2, 1], [3, 2]],
    [[-1, 1], [-1, 0], [-1, 1], [-1, 2]],
    big_random,
    big_null,
    big_self,
]

passed = 0
total = len(cases)
for n, spec in enumerate(cases, 1):
    shown = spec if len(spec) <= 10 else f"<{len(spec)} nodes>"
    try:
        got = run(spec)
        expected = [list(p) for p in spec]
        if got == expected:
            print(f"PASS case {n}")
            passed += 1
        else:
            gshow = got if len(got) <= 10 else f"<{len(got)} nodes>"
            print(f"FAIL case {n}: input={shown}, expected={shown}, got={gshow}")
    except Exception as e:
        print(f"FAIL case {n}: input={shown}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)