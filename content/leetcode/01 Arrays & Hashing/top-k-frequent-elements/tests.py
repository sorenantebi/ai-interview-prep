import sys
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


def run(nums, k):
    return ns["Solution"]().topKFrequent(list(nums), k)


def canon(res):
    return sorted(res)


# Build cases: (nums, k, expected)
cases = []
cases.append(([1, 1, 1, 2, 2, 3], 2, [1, 2]))
cases.append(([1], 1, [1]))
cases.append(([4, 4, -1, -1, -1, 7], 1, [-1]))
# all distinct, k = number of distinct
cases.append(([5, 6, 7], 3, [5, 6, 7]))
# negatives
cases.append(([-1, -1, -2, -2, -2, -3], 2, [-1, -2]))
# k=1 with a clear winner
cases.append(([3, 0, 1, 0], 1, [0]))
# boundaries of value range
cases.append(([10000, 10000, -10000, -10000, -10000, 0], 2, [10000, -10000]))
# zero values
cases.append(([0, 0, 0, 1, 1, 2], 1, [0]))
# all same
cases.append(([9] * 50, 1, [9]))
# distinct frequencies 1..5, k=3
cases.append(([1] * 5 + [2] * 4 + [3] * 3 + [4] * 2 + [5], 3, [1, 2, 3]))

# large: distinct frequencies, shuffled
rng = random.Random(12345)
big = []
exp_big = []
for idx, v in enumerate(range(-100, 100)):
    c = idx + 1
    big += [v] * c
    if idx >= 190:
        exp_big.append(v)
# total size = 200*201/2 = 20100
rng.shuffle(big)
cases.append((big, 10, exp_big))

# large: 10^5 elements, one dominant value and many singletons
big2 = [7] * 50000 + list(range(-10000, 10000)) + [8] * 30000
big2 = big2[:100000]
rng.shuffle(big2)
cases.append((big2, 2, [7, 8]))

passed = 0
total = len(cases)
for i, (nums, k, expected) in enumerate(cases, 1):
    shown = nums if len(nums) <= 30 else f"<list of {len(nums)} elements>"
    try:
        got = run(nums, k)
        if canon(got) == canon(expected):
            print(f"PASS case {i}")
            passed += 1
        else:
            print(f"FAIL case {i}: input=(nums={shown}, k={k}), expected={canon(expected)}, got={canon(got)}")
    except Exception as e:
        print(f"FAIL case {i}: input=(nums={shown}, k={k}), error={type(e).__name__}: {e}")

print(f"{passed}/{total} passed")
if passed != total:
    sys.exit(1)