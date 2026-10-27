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
    dummy = ListNode()
    cur = dummy
    for v in arr:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    queue = [root]
    i = 1
    while queue and i < len(arr):
        node = queue.pop(0)
        if i < len(arr) and arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_array(root):
    if root is None:
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


def reference(s, words):
    ws = set(words)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in ws:
                dp[i] = True
                break
    return dp[n]


cases = [
    ("leetcode", ["leet", "code"], True),
    ("applepenapple", ["apple", "pen"], True),
    ("catsandog", ["cats", "dog", "sand", "and", "cat"], False),
    ("a", ["a"], True),
    ("a", ["b"], False),
    ("aaaaaaa", ["aaaa", "aaa"], True),
    ("aaaaaaa", ["aa", "aaaa"], False),
    ("cars", ["car", "ca", "rs"], True),
    ("abcd", ["a", "abc", "b", "cd"], True),
    ("ab", ["abc"], False),
    ("goalspecial", ["go", "goal", "goals", "special"], True),
    ("a" * 299 + "b", ["a", "aa", "aaa", "aaaa", "aaaaa"], False),
    ("a" * 300, ["a" * k for k in range(1, 21)], True),
    ("ab" * 150, ["ab", "ba", "aba"], True),
]

# sanity-check expectations against the independent reference
for _s, _w, _e in cases:
    assert reference(_s, _w) == _e, (_s[:20], _e)


def short(x, limit=60):
    r = repr(x)
    return r if len(r) <= limit else r[:limit] + "..."


passed = 0
total = len(cases)
for idx, (s, words, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.wordBreak(s, list(words))
        ok = bool(got) == expected and isinstance(got, bool)
    except Exception as e:
        print(f"FAIL case {idx}: input=({short(s)}, {short(words)}), expected={expected}, got=error: {e}")
        continue
    if ok:
        print(f"PASS case {idx}")
        passed += 1
    else:
        print(f"FAIL case {idx}: input=({short(s)}, {short(words)}), expected={expected}, got={short(got)}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)