# LeetCode patterns

One card per NeetCode topic: when to reach for it, the patterns that come up most, and a template. Edit this file under Files.

## Arrays & Hashing

**Use when:** you need "have I seen X?", counts, or grouping in O(1) per lookup. For bins, also map one thing to another, for instance LinkedList1Node : LinkedList2Node.

- **Set for membership** (Contains Duplicate, Longest Consecutive: only start counting at `x` when `x - 1` is not in the set)
- **Counter / frequency map** (Valid Anagram, Top K: bucket sort by frequency gives O(n))
- **Canonical key for grouping**: sorted word or 26-count tuple (Group Anagrams)
- **Complement map**: store value → index, look up `target - x` (Two Sum)
- **Prefix / suffix products or sums** (Product Except Self) test

**How to iterate through:**
- for x in thisdict:, for x in thisdict.keys():
- for x in thisdict.values():
- for key, val in thisdict.items():

```python
seen = {}
for i, x in enumerate(nums):
    if target - x in seen:
        return [seen[target - x], i]
    seen[x] = i
```

## Two Pointers

**Use when:** the array is sorted (or can be), or you compare both ends.

- **Opposite ends, move the worse side** (Two Sum II, Container With Most Water)
- **Sort + fix one + two-pointer the rest**, skipping duplicates (3Sum)
- **Max-from-left / max-from-right** (Trapping Rain Water: move the side with the smaller max)
- **Skip non-alphanumerics, compare inward** (Valid Palindrome)

```python
l, r = 0, len(a) - 1
while l < r:
    s = a[l] + a[r]
    if s == target: return [l, r]
    if s < target: l += 1
    else: r -= 1
```

## Sliding Window

**Use when:** "longest / shortest / count of contiguous subarray or substring with property X".

- **Variable window**: grow `r`, shrink `l` while invalid (Longest Substring Without Repeating)
- **Window valid if `len - maxFreq <= k`** (Longest Repeating Character Replacement)
- **Fixed window + count match** (Permutation in String)
- **Need/have counters, shrink while valid** (Minimum Window Substring)
- **Monotonic deque of indices** for window max (Sliding Window Maximum)

```python
l = 0
for r, ch in enumerate(s):
    add(ch)
    while not valid():
        remove(s[l]); l += 1
    best = max(best, r - l + 1)
```

## Stack

**Use when:** matching pairs, "next greater/smaller", or evaluating expressions.

- **Push opens, pop on close** (Valid Parentheses)
- **Stack of (value, current min)** (Min Stack)
- **Monotonic decreasing stack of indices** → next greater element (Daily Temperatures)
- **Monotonic increasing stack** → widest rectangle (Largest Rectangle in Histogram)
- **Sort by position, stack arrival times** (Car Fleet)

```python
stack = []  # indices, values decreasing
for i, t in enumerate(temps):
    while stack and temps[stack[-1]] < t:
        j = stack.pop(); res[j] = i - j
    stack.append(i)
```

## Binary Search

**Use when:** sorted input, or the answer is monotonic ("smallest k such that ok(k)").

- **Classic `l <= r`** on a sorted array (Binary Search, Search a 2D Matrix)
- **Binary search on the answer** with a feasibility check (Koko Eating Bananas)
- **Rotated array: one half is always sorted** (Find Min / Search in Rotated Sorted Array)
- **Upper bound on timestamps** (Time Based Key-Value Store)
- **Partition the smaller array** (Median of Two Sorted Arrays)

```python
lo, hi = 1, max(piles)
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid): hi = mid
    else: lo = mid + 1
return lo
```

## Linked List

**Use when:** pointer rewiring; draw it first.

- **Dummy head** to avoid edge cases (Merge Two Lists, Remove Nth)
- **Reverse in place** with `prev, cur` (Reverse List, Reorder List, Reverse k-Group)
- **Fast / slow pointers**: middle, cycle detection, nth from end (Linked List Cycle, Find Duplicate)
- **Hash map old → new node** (Copy List With Random Pointer)
- **Hash map + doubly linked list** (LRU Cache), **heap of heads** (Merge k Lists)

```python
prev, cur = None, head
while cur:
    cur.next, prev, cur = prev, cur, cur.next
return prev
```

## Trees

**Use when:** almost always recursion: decide what each call returns.

- **DFS returning a value** up the tree: depth, diameter, balanced, max path sum
- **BFS by level** with a queue (Level Order, Right Side View)
- **Pass bounds down** (Validate BST), **pass the max so far down** (Count Good Nodes)
- **BST property** to go left or right (LCA of BST, Kth Smallest via in-order)
- **Preorder + inorder index map** (Construct Tree), **preorder with null markers** (Serialize)

```python
def dfs(node):
    if not node: return 0
    l, r = dfs(node.left), dfs(node.right)
    self.best = max(self.best, l + r)
    return 1 + max(l, r)
```

## Heap / Priority Queue

**Use when:** repeatedly needing the min/max, or "top k".

- **Min-heap of size k** → kth largest (Kth Largest in Stream / Array)
- **Max-heap via negation** (Last Stone Weight, Task Scheduler)
- **Two heaps, small max-heap + large min-heap** (Find Median from Data Stream)
- **Heap of (distance, point)** (K Closest Points)
- **Merge k sorted streams** with `(value, list index, position)` (Design Twitter)

```python
import heapq
heap = []
for x in nums:
    heapq.heappush(heap, x)
    if len(heap) > k: heapq.heappop(heap)
return heap[0]
```

## Backtracking

**Use when:** "all combinations / permutations / subsets / placements".

- **Choose / explore / un-choose** with `path.append` … `path.pop()`
- **Include-or-skip** decision tree (Subsets, Combination Sum: reuse means `i` stays)
- **Sort + skip duplicates at the same depth** (Subsets II, Combination Sum II)
- **Used-set or swap** for permutations
- **Grid DFS with a visited mark**, restore on return (Word Search); **cols / diagonals sets** (N-Queens)

```python
def dfs(i, path):
    if i == len(nums):
        res.append(path[:]); return
    path.append(nums[i]); dfs(i + 1, path)
    path.pop(); dfs(i + 1, path)
```

## Tries

**Use when:** many prefix queries over a set of words.

- **Node = dict of children + end flag** (Implement Trie)
- **`.` wildcard → DFS over all children** (Add and Search Words)
- **Trie of words + grid DFS, prune finished words** (Word Search II)

```python
class TrieNode:
    def __init__(self):
        self.children, self.end = {}, False
def insert(root, word):
    node = root
    for ch in word:
        node = node.children.setdefault(ch, TrieNode())
    node.end = True
```

## Graphs

**Use when:** grids or explicit edges: pick DFS/BFS, mark visited.

- **Flood fill** counting components (Number of Islands, Max Area)
- **Multi-source BFS** from all starts at once (Rotting Oranges, Walls and Gates)
- **Reverse thinking: start from the border/ocean** (Pacific Atlantic, Surrounded Regions)
- **Topological sort / cycle detection** (Course Schedule I & II)
- **Union-Find** (Redundant Connection, Connected Components, Graph Valid Tree)
- **BFS over word patterns** (Word Ladder)

```python
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb: return False
    parent[ra] = rb; return True
```

## Advanced Graphs

**Use when:** weighted shortest paths, minimum spanning trees, ordering constraints.

- **Dijkstra** with a min-heap (Network Delay Time, Swim in Rising Water: minimise the max)
- **Prim's / Kruskal's MST** (Min Cost to Connect All Points)
- **Bellman-Ford with k rounds** (Cheapest Flights Within K Stops)
- **Topological order from character comparisons** (Alien Dictionary)
- **Hierholzer / post-order DFS** on sorted edges (Reconstruct Itinerary)

```python
dist = {src: 0}
heap = [(0, src)]
while heap:
    d, u = heapq.heappop(heap)
    if d > dist.get(u, inf): continue
    for v, w in adj[u]:
        if d + w < dist.get(v, inf):
            dist[v] = d + w; heapq.heappush(heap, (d + w, v))
```

## 1-D Dynamic Programming

**Use when:** the answer for `i` depends on a few earlier answers.

- **`dp[i] = f(dp[i-1], dp[i-2])`** with two variables (Climbing Stairs, House Robber; Robber II = run twice)
- **Expand around center** (Longest Palindromic Substring, Palindromic Substrings)
- **Unbounded knapsack over amounts** (Coin Change), **subset-sum set** (Partition Equal Subset Sum)
- **Track both max and min** (Maximum Product Subarray)
- **`dp[i]` = can the prefix be built** (Word Break, Decode Ways); **LIS** O(n²) or patience sort

```python
prev2, prev1 = 0, 0
for x in nums:
    prev2, prev1 = prev1, max(prev1, prev2 + x)
return prev1
```

## 2-D Dynamic Programming

**Use when:** two indices (two strings, grid, item × capacity).

- **Grid paths** `dp[r][c] = dp[r-1][c] + dp[r][c-1]` (Unique Paths)
- **Two strings: match → diagonal + 1, else max/min of neighbours** (LCS, Edit Distance, Distinct Subsequences, Interleaving String)
- **State machine** (Stock With Cooldown: holding / sold / rest)
- **Count ways over amounts** (Coin Change II), **sum offsets** (Target Sum)
- **Interval DP: last balloon to burst** (Burst Balloons); **memoised DFS on grids** (Longest Increasing Path)

```python
dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
for i in range(len(a) - 1, -1, -1):
    for j in range(len(b) - 1, -1, -1):
        dp[i][j] = 1 + dp[i+1][j+1] if a[i] == b[j] else max(dp[i+1][j], dp[i][j+1])
```

## Greedy

**Use when:** a locally best choice can be proven safe.

- **Kadane: reset when the running sum goes negative** (Maximum Subarray)
- **Track the furthest reachable index** (Jump Game I & II as BFS levels)
- **If total gas ≥ total cost, start after the last failure** (Gas Station)
- **Last occurrence of each char** → cut partitions (Partition Labels)
- **Range of possible open counts** (Valid Parenthesis String); **min-heap of group starts** (Hand of Straights)

```python
best = cur = nums[0]
for x in nums[1:]:
    cur = max(x, cur + x)
    best = max(best, cur)
```

## Intervals

**Use when:** ranges overlap. Sort by start (or end) first.

- **Sort by start, merge if `start <= last_end`** (Merge Intervals, Insert Interval)
- **Sort by end, keep the earliest-ending** → minimum removals (Non-overlapping Intervals)
- **Sorted starts vs sorted ends, or a min-heap of ends** → rooms needed (Meeting Rooms II)
- **Sort queries + min-heap by size** (Minimum Interval to Include Each Query)

```python
intervals.sort()
out = [intervals[0]]
for s, e in intervals[1:]:
    if s <= out[-1][1]: out[-1][1] = max(out[-1][1], e)
    else: out.append([s, e])
```

## Math & Geometry

**Use when:** matrix manipulation or digit tricks.

- **Rotate = transpose + reverse each row** (Rotate Image)
- **Shrink four boundaries** (Spiral Matrix)
- **Use the first row/column as markers** for O(1) space (Set Matrix Zeroes)
- **Cycle detection on digit sums** (Happy Number), **carry from the end** (Plus One, Multiply Strings)
- **Fast power by squaring** (Pow(x, n)); **count points by coordinate** (Detect Squares)

```python
def pow(x, n):
    if n < 0: x, n = 1 / x, -n
    res = 1
    while n:
        if n & 1: res *= x
        x *= x; n >>= 1
    return res
```

## Bit Manipulation

**Use when:** XOR cancellation, counting bits, or arithmetic without `+`.

- **XOR everything: pairs cancel** (Single Number, Missing Number)
- **`n & (n - 1)` drops the lowest set bit** (Number of 1 Bits)
- **`dp[i] = dp[i >> 1] + (i & 1)`** (Counting Bits)
- **Shift out / shift in 32 times** (Reverse Bits)
- **Sum = XOR, carry = AND << 1**, mask to 32 bits in Python (Sum of Two Integers)

```python
count = 0
while n:
    n &= n - 1
    count += 1
```

## Complexity

**O(n * m) vs O(n + m):**

nested loops: 
```python
for x in a:          # runs n times
    for c in x:     
            
```

if you do the operations separately, its n + m
```python
for x in a:

for y in b:
```
