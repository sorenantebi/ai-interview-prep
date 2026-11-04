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
        n = queue.pop(0)
        if i < len(vals) and vals[i] is not None:
            n.left = TreeNode(vals[i])
            queue.append(n.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            n.right = TreeNode(vals[i])
            queue.append(n.right)
        i += 1
    return root


def tree_to_array(root):
    if not root:
        return []
    out = []
    queue = [root]
    while queue:
        n = queue.pop(0)
        if n is None:
            out.append(None)
        else:
            out.append(n.val)
            queue.append(n.left)
            queue.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out


ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
exec(open("attempt.py").read(), ns)

# large case: products "a"*k for k in 1..140, search word of 200 'a's
large_products = ["a" * k for k in range(1, 141)]
large_word = "a" * 200
large_expected = []
for i in range(1, 201):
    if i <= 140:
        large_expected.append(["a" * j for j in range(i, min(i + 2, 140) + 1)])
    else:
        large_expected.append([])

cases = [
    # 1: example 1
    (["mobile", "mouse", "moneypot", "monitor", "mousepad"], "mouse",
     [["mobile", "moneypot", "monitor"], ["mobile", "moneypot", "monitor"],
      ["mouse", "mousepad"], ["mouse", "mousepad"], ["mouse", "mousepad"]]),
    # 2: example 2
    (["havana"], "havana", [["havana"]] * 6),
    # 3: example 3
    (["bags", "baggage", "banner", "box", "cloths"], "bags",
     [["baggage", "bags", "banner"], ["baggage", "bags", "banner"], ["baggage", "bags"], ["bags"]]),
    # 4: no match at all
    (["abc"], "xyz", [[], [], []]),
    # 5: diverging from many matches
    (["abc", "abd", "abe", "abf"], "abz",
     [["abc", "abd", "abe"], ["abc", "abd", "abe"], []]),
    # 6: search word longer than product
    (["a"], "abc", [["a"], [], []]),
    # 7: products that are prefixes of each other
    (["a", "aa", "aaa", "aaaa"], "aaaa",
     [["a", "aa", "aaa"], ["aa", "aaa", "aaaa"], ["aaa", "aaaa"], ["aaaa"]]),
    # 8: unsorted input
    (["zebra", "apple", "apply", "app", "ape"], "app",
     [["ape", "app", "apple"], ["ape", "app", "apple"], ["app", "apple", "apply"]]),
    # 9: exactly three matches
    (["cat", "car", "cap"], "ca",
     [["cap", "car", "cat"], ["cap", "car", "cat"]]),
    # 10: reverse-ordered same-prefix products
    (["bd", "bc", "bb", "ba"], "b", [["ba", "bb", "bc"]]),
    # 11: single char products, single char word
    (["d", "a", "c", "b"], "a", [["a"]]),
    # 12: large input
    (large_products, large_word, large_expected),
]


def main():
    passed = 0
    total = len(cases)
    for idx, (products, word, expected) in enumerate(cases, 1):
        shown = (products if len(products) <= 10 else f"<{len(products)} products>",
                 word if len(word) <= 20 else f"<len {len(word)}>")
        try:
            got = ns["Solution"]().suggestedProducts(list(products), word)
            got_norm = [list(x) for x in got]
            if got_norm == expected:
                print(f"PASS case {idx}")
                passed += 1
            else:
                exp_s = expected if len(str(expected)) < 300 else "<large>"
                got_s = got_norm if len(str(got_norm)) < 300 else "<large>"
                print(f"FAIL case {idx}: input={shown}, expected={exp_s}, got={got_s}")
        except Exception as e:
            print(f"FAIL case {idx}: input={shown}, error={type(e).__name__}: {e}")
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


main()