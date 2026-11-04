---
topic: "Two Pointers"
difficulty: Easy
leetcode: https://leetcode.com/problems/reverse-string/
neetcode: https://neetcode.io/problems/reverse-string
---
# Reverse String - Solution

## Intuition

Reversing an array means the first element swaps with the last, the second with the second-to-last, and so on. Each pair can be swapped independently, so two pointers moving toward each other from both ends do the whole job with no extra storage.

## Approach

1. Set `left = 0` and `right = len(s) - 1`.
2. While `left < right`, swap `s[left]` and `s[right]`.
3. Move `left` forward and `right` backward by one.
4. When the pointers meet or cross, the array is reversed. A middle element in an odd-length array stays in place.

## Code

```python
class Solution:
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        l = 0
        r = len(s) - 1
        while l < r:
            s[l],s[r] = s[r],s[l]
            l += 1
            r -= 1
```

## Complexity

- **Time:** `O(n)` — each element is visited once, with n/2 swaps.
- **Space:** `O(1)` — only two index variables are used; the array is modified in place.

## Other Approaches

- **Recursion:** swap the outer pair, then recurse on the inner range — Time `O(n)` / Space `O(n)` for the call stack
- **Stack:** push all characters, then pop them back into the array — Time `O(n)` / Space `O(n)`
- **Built-in `s.reverse()` / `s[:] = s[::-1]`:** concise, but `s.reverse()` is the only one that is truly in-place; the slice form allocates a copy — Time `O(n)` / Space `O(1)` for `reverse()`, `O(n)` for the slice

## C++

```cpp
class Solution {
public:
    void reverseString(vector<char>& s) {
        int left = 0, right = s.size() - 1;
        
        while (left < right){
            swap(s[left], s[right]);
            
            left++;
            right--;
        }
    }
};
```
