import sys
from typing import List, Optional, Dict
from collections import Counter


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


def reference(candidates, target):
    """Independent counter-based DFS used to compute expected output for big inputs."""
    items = sorted(Counter(candidates).items())
    res = []

    def dfs(idx, remaining, path):
        if remaining == 0:
            res.append(list(path))
            return
        if idx == len(items):
            return
        val, cnt = items[idx]
        for k in range(0, cnt + 1):
            if k * val > remaining:
                break
            dfs(idx + 1, remaining - k * val, path + [val] * k)

    dfs(0, target, [])
    return res


def canon(result):
    # No dedupe here: duplicate combinations in the output must be detected.
    return sorted(tuple(sorted(c)) for c in result)


cases = [
    ([10, 1, 2, 7, 6, 1, 5], 8, [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]),
    ([2, 5, 2, 1, 2], 5, [[1, 2, 2], [5]]),
    ([5], 5, [[5]]),
    ([3], 5, []),
    ([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 3, [[1, 1, 1]]),
    ([2, 4, 6], 1, []),
    ([1, 2, 3], 6, [[1, 2, 3]]),
    ([1, 1, 2, 2], 4, [[1, 1, 2], [2, 2]]),
    ([50, 40, 30], 30, [[30]]),
    ([2, 2, 2, 2], 4, [[2, 2]]),
    ([1] * 100, 30, [[1] * 30]),
    (list(range(1, 51)) + list(range(1, 51)), 30, None),
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 2, 30, None),
]

passed = 0
total = len(cases)
for n, (cands, target, expected) in enumerate(cases, 1):
    if expected is None:
        expected = reference(cands, target)
    try:
        sol = ns["Solution"]()
        got = sol.combinationSum2(list(cands), target)
        ok = canon(got) == canon(expected)
    except Exception as e:
        print(f"FAIL case {n}: input=({cands if len(cands) <= 20 else '...len=' + str(len(cands))}, {target}), error={type(e).__name__}: {e}")
        continue
    if ok:
        passed += 1
        print(f"PASS case {n}")
    else:
        shown = cands if len(cands) <= 20 else f"...len={len(cands)}"
        exp_s = canon(expected)
        got_s = canon(got)
        if len(exp_s) > 10:
            exp_s = f"{len(exp_s)} combos"
        if len(got_s) > 10:
            got_s = f"{len(got_s)} combos"
        print(f"FAIL case {n}: input=({shown}, {target}), expected={exp_s}, got={got_s}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)