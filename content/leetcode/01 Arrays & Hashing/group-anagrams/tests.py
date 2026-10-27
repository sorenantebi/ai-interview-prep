import sys
import collections
import string
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


def build_list(arr):
    head = None
    for v in reversed(arr):
        head = ListNode(v, head)
    return head


def list_to_array(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def build_tree(arr):
    if not arr or arr[0] is None:
        return None
    root = TreeNode(arr[0])
    queue = collections.deque([root])
    i = 1
    while queue and i < len(arr):
        node = queue.popleft()
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
    queue = collections.deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {
    "ListNode": ListNode,
    "TreeNode": TreeNode,
    "List": List,
    "Optional": Optional,
    "Dict": Dict,
    "collections": collections,
    "defaultdict": collections.defaultdict,
}
exec(open("attempt.py").read(), ns)


def canon(groups):
    return sorted(sorted(g) for g in groups)


def make_large():
    rng = random.Random(12345)
    words = []
    for _ in range(10000):
        n = rng.randint(0, 100)
        words.append("".join(rng.choice(string.ascii_lowercase) for _ in range(n)))
    return words


def make_large_anagrams():
    rng = random.Random(7)
    base = "".join(rng.choice(string.ascii_lowercase) for _ in range(100))
    words = []
    for _ in range(5000):
        chars = list(base)
        rng.shuffle(chars)
        words.append("".join(chars))
    return words


cases = [
    (["eat", "tea", "tan", "ate", "nat", "bat"], [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]),
    ([""], [[""]]),
    (["abc", "bca", "xyz"], [["abc", "bca"], ["xyz"]]),
    (["a"], [["a"]]),
    (["", "", ""], [["", "", ""]]),
    (["a", "b", "c"], [["a"], ["b"], ["c"]]),
    (["abc", "abc", "cba", "bac"], [["abc", "abc", "cba", "bac"]]),
    (["aab", "aba", "baa", "abb", "bab", "bba"], [["aab", "aba", "baa"], ["abb", "bab", "bba"]]),
    (["ab", "abb", "ba"], [["ab", "ba"], ["abb"]]),
    (["", "a", ""], [["", ""], ["a"]]),
]

# Large: many words, groups computed with the sorted-key approach
large = make_large()
ref = {}
for w in large:
    ref.setdefault("".join(sorted(w)), []).append(w)
cases.append((large, list(ref.values())))

# Large: all anagrams of the same word, one group
big_anagrams = make_large_anagrams()
cases.append((big_anagrams, [big_anagrams]))


def show(strs):
    if len(strs) > 10:
        return f"<{len(strs)} strings>"
    return repr(strs)


passed = 0
total = len(cases)
for i, (strs, expected) in enumerate(cases, 1):
    try:
        sol = ns["Solution"]()
        got = sol.groupAnagrams(list(strs))
        if canon(got) == canon(expected):
            print(f"PASS case {i}")
            passed += 1
        else:
            if len(strs) > 10:
                print(f"FAIL case {i}: input={show(strs)}, expected={len(expected)} groups, got={len(got)} groups")
            else:
                print(f"FAIL case {i}: input={show(strs)}, expected={canon(expected)}, got={canon(got)}")
    except Exception as e:
        print(f"FAIL case {i}: input={show(strs)}, error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)
