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


def reference(coins, amount):
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
    return dp[amount] if dp[amount] != amount + 1 else -1


cases = [
    ([1, 2, 5], 11, 3),
    ([2], 3, -1),
    ([1], 0, 0),
    ([1], 1, 1),
    ([1], 2, 2),
    ([1, 3, 4], 6, 2),
    ([2], 4, 2),
    ([2, 5, 10, 1], 27, 4),
    ([186, 419, 83, 408], 6249, 20),
    ([2147483647], 2, -1),
    ([5, 7], 3, -1),
    ([3, 7, 405, 436], 8839, 25),
    ([1, 2, 5], 10000, 2000),
    ([2, 4, 6, 8], 9999, -1),
    ([7, 13, 29, 101, 2147483647], 10000, reference([7, 13, 29, 101, 2147483647], 10000)),
]


def main():
    passed = 0
    total = len(cases)
    for n, (coins, amount, expected) in enumerate(cases, 1):
        try:
            sol = ns["Solution"]()
            got = sol.coinChange(list(coins), amount)
            if got == expected:
                print(f"PASS case {n}")
                passed += 1
            else:
                print(f"FAIL case {n}: input=coins={coins}, amount={amount}, expected={expected}, got={got}")
        except Exception as e:
            print(f"FAIL case {n}: input=coins={coins}, amount={amount}, error={type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()