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
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = [root]
    i = 1
    while queue and i < len(vals):
        node = queue.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
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


def solve(words):
    return ns["Solution"]().alienOrder(list(words))


def check(words, valid, got):
    """Any valid order is accepted; invalid inputs must return ''."""
    if not valid:
        return got == ""
    letters = set("".join(words))
    if not isinstance(got, str) or len(got) != len(letters) or set(got) != letters:
        return False
    pos = {c: i for i, c in enumerate(got)}
    for w1, w2 in zip(words, words[1:]):
        for a, b in zip(w1, w2):
            if a != b:
                if pos[a] >= pos[b]:
                    return False
                break
    return True


perm = "qwertyuiopasdfghjklzxcvbnm"

cases = [
    (["wrt", "wrf", "er", "ett", "rftt"], True),   # example 1
    (["z", "x"], True),                            # example 2
    (["z", "x", "z"], False),                      # example 3
    (["abc", "ab"], False),                        # longer word before its prefix
    (["ab", "abc"], True),                         # valid prefix order
    (["abc"], True),                               # single word
    (["a"], True),                                 # single letter
    (["a", "a"], True),                            # duplicates
    (["a", "b", "c", "a"], False),                 # 3-cycle via non-adjacent facts
    (["ba", "bc", "ac", "ab"], False),             # cycle a<c<b<a
    (["ab", "cd"], True),                          # unconstrained letters
    (["abc", "abd"], True),                        # only last letters differ
    ([c for c in perm], True),                     # all 26 letters, full chain
    (["a" * 100] * 50 + ["b" * 100] * 50, True),   # long words, many duplicates
    ([perm[:i] for i in range(26, 0, -1)], False), # decreasing prefixes -> invalid
]

passed = 0
total = len(cases)
for n, (words, valid) in enumerate(cases, 1):
    try:
        got = solve(words)
        ok = check(words, valid, got)
    except Exception as e:
        print(f"FAIL case {n}: input={words}, error={type(e).__name__}: {e}")
        continue
    if ok:
        passed += 1
        print(f"PASS case {n}")
    else:
        exp = "any valid order" if valid else '""'
        print(f"FAIL case {n}: input={words}, expected={exp}, got={got!r}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)