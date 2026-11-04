---
topic: "Stack"
difficulty: Easy
leetcode: https://leetcode.com/problems/baseball-game/
neetcode: https://neetcode.io/problems/baseball-game
---
# Baseball Game - Solution

## Intuition

Every operation only looks at, or removes, the most recent scores on the record. That is last-in-first-out behavior, so a stack models the record directly.

## Approach

1. Keep a stack of valid scores.
2. For each operation:
   - `"+"`: push the sum of the top two scores.
   - `"D"`: push double the top score.
   - `"C"`: pop the top score.
   - Otherwise: convert the string to an integer and push it.
3. After processing all operations, return the sum of the stack.

## Code

```python
class Solution:
    def calPoints(self, operations: List[str]) -> int:
        
        score_stack = []
        
        for o in operations:
            
            # it is +, D, or C
            # if stack isn't of sufficient length, then operation is voided
            if o == "+" and len(score_stack) >= 2:
                summed = score_stack[-2] + score_stack[-1]
                score_stack.append(summed)
                
            elif o == "D" and len(score_stack) >= 1:
                doubled = score_stack[-1] * 2
                score_stack.append(doubled)
                
            elif o == "C" and len(score_stack) >= 1:
                score_stack.pop() 
                
            else: 
                score_stack.append(int(o))

        return sum(score_stack)
```

## Complexity

- **Time:** `O(n)` — each operation does constant work, and the final sum is a single pass over at most `n` scores.
- **Space:** `O(n)` — the stack can hold up to `n` scores.

## Other Approaches

- **Running total with a stack:** maintain a running sum, adjusting it on each push and pop instead of summing at the end — Time `O(n)` / Space `O(n)`

## C++

```cpp
class Solution {
public:
    int calPoints(vector<string>& ops) {
        stack<int> stack;
        int sum =  0;
        
        for (int i = 0; i < ops.size(); i++){
            if (ops[i] == "+"){
                int first = stack.top();
                stack.pop();
                
                int second = stack.top();
                
                stack.push(first);
                
                stack.push(first + second);
                
                sum += first + second;
            }
            
            else if (ops[i] == "D"){
                sum += 2 * stack.top();
                stack.push(2 * stack.top());
            }
            
            else if (ops[i] == "C"){
                sum -= stack.top();
                stack.pop();
            }
            
            else{
                sum += stoi(ops[i]);
                stack.push(stoi(ops[i]));
            }
        }
        
        return sum;
        
        
    }
};
```
