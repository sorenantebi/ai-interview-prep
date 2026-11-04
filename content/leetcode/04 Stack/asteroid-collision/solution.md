---
topic: "Stack"
difficulty: Medium
leetcode: https://leetcode.com/problems/asteroid-collision/
neetcode: https://neetcode.io/problems/asteroid-collision
---
# Asteroid Collision - Solution

## Intuition

A collision only happens when a right-moving asteroid is immediately followed by a left-moving one. So the only asteroids that can still be hit by a new left-moving asteroid are the right-movers sitting at the end of the surviving row. That "most recent survivor" structure is exactly a stack.

## Approach

1. Keep a stack of surviving asteroids.
2. For each asteroid `a`, while `a` is moving left and the stack top is moving right, resolve a collision:
   - If the top is smaller, pop it and continue checking `a` against the new top.
   - If the top is equal in size, pop it and `a` also explodes.
   - If the top is larger, `a` explodes.
3. If `a` survived all collisions, push it.
4. After processing everything, the stack is the answer.

## Code

```python
class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        stack = []

        for a in asteroids:
            while stack and a < 0 and stack[-1] > 0:
                diff = a + stack[-1]
                if diff > 0:
                    a = 0
                elif diff < 0:
                    stack.pop()
                else:
                    a = 0
                    stack.pop()
            if a:
                stack.append(a)

        return stack
```

## Complexity

- **Time:** `O(n)` — each asteroid is pushed at most once and popped at most once.
- **Space:** `O(n)` — the stack can hold all asteroids when none collide.

## Other Approaches

- **Brute-force simulation:** repeatedly scan the array and resolve adjacent right/left pairs until nothing changes — Time `O(n^2)` / Space `O(n)`

## C++

```cpp
class Solution {
public:
    vector<int> asteroidCollision(vector<int>& asteroids) {
        vector<int> stk;

        for (auto ast: asteroids)
        {
            while (!stk.empty() && stk.back() > 0 && ast < 0)
            {
                int diff = ast + stk.back();
                if (diff > 0)
                {
                    ast = 0;
                }
                else if (diff < 0)
                {
                    stk.pop_back();
                }
                else
                {
                    ast = 0;
                    stk.pop_back();
                } 
            }
            if (ast != 0)
                stk.push_back(ast);
        }
        return stk;
    }
};
```
