import sys
import copy
from typing import List, Optional, Dict, Set, Tuple
from collections import defaultdict, deque, Counter


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


ns = {
    "ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional,
    "Dict": Dict, "Set": Set, "Tuple": Tuple, "defaultdict": defaultdict,
    "deque": deque, "Counter": Counter,
}
exec(open("attempt.py").read(), ns)


def canon(res):
    return sorted([list(r) for r in res])


def short(x, limit=200):
    s = repr(x)
    return s if len(s) <= limit else s[:limit] + "...(truncated)"


cases = []

# 1: example 1
cases.append((
    [["John", "johnsmith@mail.com", "john_newyork@mail.com"],
     ["John", "johnsmith@mail.com", "john00@mail.com"],
     ["Mary", "mary@mail.com"],
     ["John", "johnnybravo@mail.com"]],
    [["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
     ["Mary", "mary@mail.com"],
     ["John", "johnnybravo@mail.com"]],
))

# 2: example 2
cases.append((
    [["Gabe", "Gabe0@m.co", "Gabe3@m.co", "Gabe1@m.co"],
     ["Kevin", "Kevin3@m.co", "Kevin5@m.co", "Kevin0@m.co"],
     ["Ethan", "Ethan5@m.co", "Ethan4@m.co", "Ethan0@m.co"],
     ["Hanzo", "Hanzo3@m.co", "Hanzo1@m.co", "Hanzo0@m.co"],
     ["Fern", "Fern5@m.co", "Fern1@m.co", "Fern0@m.co"]],
    [["Ethan", "Ethan0@m.co", "Ethan4@m.co", "Ethan5@m.co"],
     ["Gabe", "Gabe0@m.co", "Gabe1@m.co", "Gabe3@m.co"],
     ["Hanzo", "Hanzo0@m.co", "Hanzo1@m.co", "Hanzo3@m.co"],
     ["Kevin", "Kevin0@m.co", "Kevin3@m.co", "Kevin5@m.co"],
     ["Fern", "Fern0@m.co", "Fern1@m.co", "Fern5@m.co"]],
))

# 3: single account, unsorted emails
cases.append((
    [["Solo", "z@m.co", "a@m.co", "m@m.co"]],
    [["Solo", "a@m.co", "m@m.co", "z@m.co"]],
))

# 4: transitive merge through a bridging account
cases.append((
    [["A", "e1@m.co", "e2@m.co"],
     ["A", "e3@m.co", "e4@m.co"],
     ["A", "e2@m.co", "e3@m.co"]],
    [["A", "e1@m.co", "e2@m.co", "e3@m.co", "e4@m.co"]],
))

# 5: same name, no shared emails -> stay separate
cases.append((
    [["John", "j1@m.co"], ["John", "j2@m.co"]],
    [["John", "j1@m.co"], ["John", "j2@m.co"]],
))

# 6: duplicate email inside one account
cases.append((
    [["A", "x@m.co", "x@m.co"]],
    [["A", "x@m.co"]],
))

# 7: later account bridges two earlier ones
cases.append((
    [["A", "a@m.co"], ["A", "b@m.co"], ["A", "a@m.co", "b@m.co"]],
    [["A", "a@m.co", "b@m.co"]],
))

# 8: mixed names, merge across non-adjacent accounts
cases.append((
    [["Bob", "b1@m.co"], ["Alice", "a1@m.co"], ["Bob", "b2@m.co", "b1@m.co"]],
    [["Bob", "b1@m.co", "b2@m.co"], ["Alice", "a1@m.co"]],
))

# 9: ASCII sort order (uppercase before lowercase)
cases.append((
    [["A", "b@m.co", "B@m.co"]],
    [["A", "B@m.co", "b@m.co"]],
))

# 10: large chain of 1000 accounts merging into one
chain_in = [["Chain", f"u{i}@m.co", f"u{i+1}@m.co"] for i in range(1000)]
chain_out = [["Chain"] + sorted(f"u{i}@m.co" for i in range(1001))]
cases.append((chain_in, chain_out))

# 11: large with no merging, 1000 accounts x 9 emails
big_in = []
big_out = []
for i in range(1000):
    emails = [f"p{i}_{j}@m.co" for j in range(9)]
    big_in.append([f"N{i}"] + emails[::-1])
    big_out.append([f"N{i}"] + sorted(emails))
cases.append((big_in, big_out))

# 12: star: all accounts share a hub email, reverse order of insertion
star_in = [["S", "hub@m.co", f"s{i}@m.co"] for i in range(500)]
star_out = [["S"] + sorted(["hub@m.co"] + [f"s{i}@m.co" for i in range(500)])]
cases.append((star_in, star_out))

# 13: two separate groups with the same name plus a lone one
cases.append((
    [["J", "a@m.co", "b@m.co"], ["J", "c@m.co", "d@m.co"],
     ["J", "b@m.co", "e@m.co"], ["J", "d@m.co", "f@m.co"], ["J", "g@m.co"]],
    [["J", "a@m.co", "b@m.co", "e@m.co"],
     ["J", "c@m.co", "d@m.co", "f@m.co"],
     ["J", "g@m.co"]],
))

passed = 0
total = len(cases)
for n, (inp, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.accountsMerge(copy.deepcopy(inp))
        if canon(got) == canon(expected):
            print(f"PASS case {n}")
            passed += 1
        else:
            print(f"FAIL case {n}: input={short(inp)}, expected={short(canon(expected))}, got={short(canon(got))}")
    except Exception as e:
        print(f"FAIL case {n}: input={short(inp)}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)