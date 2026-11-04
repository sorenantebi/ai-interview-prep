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

cases = [
    ("leetscode", ["leet", "code", "leetcode"], 1),
    ("sayhelloworld", ["hello", "world"], 3),
    ("a", ["a"], 0),
    ("a", ["b"], 1),
    ("abc", ["d"], 3),
    ("aaaa", ["aa"], 0),
    ("aaaaa", ["aa"], 1),
    ("abcde", ["abcde", "ab", "cde"], 0),
    ("applepenapple", ["apple", "pen"], 0),
    ("catsandog", ["cats", "dog", "sand", "and", "cat"], 2),
    ("abcd", ["ab", "bcd"], 1),
    ("a" * 50, ["a" * 13, "a" * 17], 3),
    ("a" * 49, ["a" * 7, "a" * 11], 0),
]

passed = 0
total = len(cases)
for idx, (s, dictionary, expected) in enumerate(cases, 1):
    try:
        got = ns["Solution"]().minExtraChar(s, list(dictionary))
        if got == expected:
            print(f"PASS case {idx}")
            passed += 1
        else:
            print(f"FAIL case {idx}: input=({s!r}, {dictionary!r}), expected={expected!r}, got={got!r}")
    except Exception as e:
        print(f"FAIL case {idx}: input=({s!r}, {dictionary!r}), expected={expected!r}, got=Exception: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)