---
topic: "Tries"
difficulty: Medium
leetcode: https://leetcode.com/problems/search-suggestions-system/
---
# Search Suggestions System - Solution

## Intuition

Each typed prefix matches one node in a trie built from the products. If we insert the products in sorted order, the first three words that pass through a node are the three smallest words with that prefix. So each node can store its suggestion list while the trie is being built, and each query is then a single walk down the trie.

## Approach

1. Sort `products` lexicographically.
2. Insert each product into a trie. At every node on the word's path, add the word to that node's suggestion list if the list holds fewer than three words.
3. Walk the trie one character of `searchWord` at a time. Once a character has no matching child, every longer prefix also has no matches, so keep using an empty node.
4. After each character, record the current node's suggestion list. If there is no node, record an empty list.

## Code

```python
from typing import List, Optional

class Solution:
	def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
		root = {}
		for word in sorted(products):
			node = root
			for c in word:
				node = node.setdefault(c, {})
				# "#" can't clash with a lowercase letter key
				suggestions = node.setdefault("#", [])
				# sorted insertion means the first 3 seen are the smallest
				if len(suggestions) < 3:
					suggestions.append(word)

		res = []
		node = root
		for c in searchWord:
			# once a prefix misses, node stays {} for the rest
			node = node.get(c, {})
			res.append(node.get("#", []))
		return res
```

## Complexity

- **Time:** `O(S log n + L)`. Here `S` is the total number of characters across products, `n` is the number of products and `L` is `len(searchWord)`. Sorting does `O(n log n)` comparisons, and each comparison can read up to a full word's length. Building the trie reads every character once, and each query step takes constant time.
- **Space:** `O(S)`. The trie has at most one node per product character, and each node stores at most three word references.

## Other Approaches

- **Sort + binary search:** Sort the products. For each prefix, use `bisect_left` to find the first candidate, then check up to the next 3 words to see if they start with the prefix. Time `O(S log n + L · (log n · L))` / Space `O(1)` extra, not counting the sort.
- **Sort + two pointers:** Keep a window `[l, r]` over the sorted products. After each character, shrink the window from both ends to drop words that don't match at that position, then take up to 3 words from `l`. Time `O(S log n + n + L)` / Space `O(1)` extra.
