---
topic: "Tries"
difficulty: Medium
leetcode: https://leetcode.com/problems/search-suggestions-system/
---
# Search Suggestions System

**Topic:** Tries · **Difficulty:** Medium

## Problem

You get an array of strings `products` and a string `searchWord`. Build a suggestion feature that runs as the user types `searchWord` one character at a time.

After each character is typed, suggest up to three products whose names start with the prefix typed so far. If more than three products match, return the three that come first in lexicographical order.

Return a list of lists. The `i`-th list holds the suggestions shown after the first `i + 1` characters of `searchWord` are typed.

## Examples

**Example 1**
```text
Input: products = ["mobile","mouse","moneypot","monitor","mousepad"], searchWord = "mouse"
Output: [["mobile","moneypot","monitor"],["mobile","moneypot","monitor"],["mouse","mousepad"],["mouse","mousepad"],["mouse","mousepad"]]
Explanation: In sorted order the products are ["mobile","moneypot","monitor","mouse","mousepad"].
After typing "m" and "mo", every product matches, so the first three are suggested.
After typing "mou", "mous" and "mouse", only "mouse" and "mousepad" match.
```

**Example 2**
```text
Input: products = ["havana"], searchWord = "havana"
Output: [["havana"],["havana"],["havana"],["havana"],["havana"],["havana"]]
Explanation: "havana" matches every prefix that is typed.
```

**Example 3**
```text
Input: products = ["bags","baggage","banner","box","cloths"], searchWord = "bags"
Output: [["baggage","bags","banner"],["baggage","bags","banner"],["baggage","bags"],["bags"]]
```

## Constraints

- `1 <= products.length <= 1000`
- `1 <= products[i].length <= 3000`
- `1 <= sum(products[i].length) <= 2 * 10^4`
- All strings in `products` are unique.
- `products[i]` consists of lowercase English letters.
- `1 <= searchWord.length <= 1000`
- `searchWord` consists of lowercase English letters.
