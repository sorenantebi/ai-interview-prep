import sys
import random
from copy import deepcopy
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


def list_to_array(head):
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


def tree_to_array(root):
    out = []
    queue = [root]
    while queue:
        node = queue.pop(0)
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


def reference(tickets):
    adj = {}
    for src, dst in tickets:
        adj.setdefault(src, []).append(dst)
    for k in adj:
        adj[k].sort(reverse=True)
    stack = ["JFK"]
    route = []
    while stack:
        while adj.get(stack[-1]):
            stack.append(adj[stack[-1]].pop())
        route.append(stack.pop())
    return route[::-1]


def code(i):
    return "X" + chr(65 + i // 26) + chr(65 + i % 26)


def chain_case():
    n = 300
    names = ["JFK"] + [code(i) for i in range(n)]
    tickets = [[names[i], names[i + 1]] for i in range(n)]
    random.Random(1).shuffle(tickets)
    return tickets, names


def pingpong_case():
    tickets = [["JFK", "AAA"]] * 149 + [["AAA", "JFK"]] * 149 + [["JFK", "ZZZ"]]
    tickets = [list(t) for t in tickets]
    random.Random(2).shuffle(tickets)
    expected = ["JFK"] + ["AAA", "JFK"] * 149 + ["ZZZ"]
    return tickets, expected


def random_walk_case(seed, steps, airports):
    rng = random.Random(seed)
    cur = "JFK"
    tickets = []
    for _ in range(steps):
        nxt = rng.choice([a for a in airports if a != cur])
        tickets.append([cur, nxt])
        cur = nxt
    rng.shuffle(tickets)
    return tickets


chain_tickets, chain_expected = chain_case()
pp_tickets, pp_expected = pingpong_case()
walk_airports = ["JFK", "ATL", "SFO", "LAX", "ORD", "MUC", "LHR", "NRT"]
walk_tickets = random_walk_case(7, 300, walk_airports)
walk_small = random_walk_case(11, 12, walk_airports[:4])

cases = [
    # examples
    ([["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]],
     ["JFK", "MUC", "LHR", "SFO", "SJC"]),
    ([["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]],
     ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"]),
    ([["JFK", "KUL"], ["JFK", "NRT"], ["NRT", "JFK"]],
     ["JFK", "NRT", "JFK", "KUL"]),
    # single ticket
    ([["JFK", "AAA"]], ["JFK", "AAA"]),
    # duplicate tickets
    ([["JFK", "SFO"], ["JFK", "SFO"], ["SFO", "JFK"]],
     ["JFK", "SFO", "JFK", "SFO"]),
    # two loops through JFK
    ([["JFK", "BBB"], ["BBB", "JFK"], ["JFK", "AAA"], ["AAA", "JFK"]],
     ["JFK", "AAA", "JFK", "BBB", "JFK"]),
    # smaller destination is a dead end
    ([["JFK", "AAA"], ["JFK", "BBB"], ["BBB", "JFK"]],
     ["JFK", "BBB", "JFK", "AAA"]),
    # dead-end branch of length 2
    ([["JFK", "AAA"], ["AAA", "BBB"], ["JFK", "CCC"], ["CCC", "JFK"]],
     ["JFK", "CCC", "JFK", "AAA", "BBB"]),
    # large: long chain, shuffled input
    (chain_tickets, chain_expected),
    # large: many repeated round trips
    (pp_tickets, pp_expected),
    # random Eulerian walk, small
    (walk_small, reference(walk_small)),
    # random Eulerian walk, 300 tickets
    (walk_tickets, reference(walk_tickets)),
]

passed = 0
total = len(cases)
for i, (tickets, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().findItinerary(deepcopy(tickets))
        if got == expected:
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input={tickets}, expected={expected}, got={got}")
    except Exception as e:
        print(f"FAIL case {i}: input={tickets}, expected={expected}, got=exception: {e!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)