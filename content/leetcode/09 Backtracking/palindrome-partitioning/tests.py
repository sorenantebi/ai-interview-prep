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


def reference(s):
    n = len(s)
    res = []

    def dfs(i, path):
        if i == n:
            res.append(list(path))
            return
        for j in range(i, n):
            sub = s[i:j + 1]
            if sub == sub[::-1]:
                path.append(sub)
                dfs(j + 1, path)
                path.pop()

    dfs(0, [])
    return res


def canon(result):
    return sorted([list(p) for p in result])


cases = [
    ("aab", [["a", "a", "b"], ["aa", "b"]]),
    ("a", [["a"]]),
    ("ab", [["a", "b"]]),
    ("aa", [["a", "a"], ["aa"]]),
    ("aaa", [["a", "a", "a"], ["a", "aa"], ["aa", "a"], ["aaa"]]),
    ("aba", [["a", "b", "a"], ["aba"]]),
    ("abc", [["a", "b", "c"]]),
    ("abba", [["a", "b", "b", "a"], ["a", "bb", "a"], ["abba"]]),
    ("racecar", None),
    ("abcdefg", [list("abcdefg")]),
    ("abacaba", None),
    ("aaaaaaaaaaaaaaaa", None),  # length 16, 2^15 partitions
    ("aabbaabbaabbaabb", None),
]

passed = 0
total = len(cases)
for idx, (s, expected) in enumerate(cases, 1):
    if expected is None:
        expected = reference(s)
    try:
        got = ns["Solution"]().partition(s)
        if canon(got) == canon(expected):
            print(f"PASS case {idx}")
            passed += 1
        else:
            shown_got = got if len(str(got)) < 300 else f"<{len(got)} partitions>"
            shown_exp = expected if len(str(expected)) < 300 else f"<{len(expected)} partitions>"
            print(f"FAIL case {idx}: input={s!r}, expected={shown_exp}, got={shown_got}")
    except Exception as e:
        print(f"FAIL case {idx}: input={s!r}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)