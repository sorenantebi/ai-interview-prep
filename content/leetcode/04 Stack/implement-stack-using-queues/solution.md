---
topic: "Stack"
difficulty: Easy
leetcode: https://leetcode.com/problems/implement-stack-using-queues/
neetcode: https://neetcode.io/problems/implement-stack-using-queues
---
# Implement Stack using Queues - Solution

## Intuition

A queue is FIFO and a stack is LIFO, so the newest element must be at the front of the queue to be popped first. If every `push` rotates the queue so the new element ends up at the front, then `pop` and `top` become plain front operations.

## Approach

1. Keep a single queue.
2. On `push(x)`, append `x` to the back, then move the `len - 1` elements that were already there from the front to the back. Now `x` is at the front.
3. `pop()` removes and returns the front element.
4. `top()` returns the front element without removing it.
5. `empty()` checks whether the queue is empty.

## Code

```python
class MyStack:
    def __init__(self):
        self.q = deque()

    def push(self, x: int) -> None:
        self.q.append(x)
        
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())

    def pop(self) -> int:
        return self.q.popleft()

    def top(self) -> int:
        return self.q[0]

    def empty(self) -> bool:
        return len(self.q) == 0
```

## Complexity

- **Time:** `O(n)` for `push`, `O(1)` for `pop`, `top`, and `empty` — `push` rotates the `n - 1` existing elements; the others touch only the front.
- **Space:** `O(n)` — all elements are stored in one queue.

## Other Approaches

- **Two queues, expensive push:** push into an empty helper queue, then drain the main queue into it behind the new element and swap — Time `O(n)` push, `O(1)` others / Space `O(n)`
- **Two queues, expensive pop:** push to the back in `O(1)`; on pop, move all but the last element to the helper queue, return the last, then swap — Time `O(1)` push, `O(n)` pop/top / Space `O(n)`

## C++

```cpp
/*
Implement a last-in-first-out (LIFO) stack using only two queues. The implemented stack should support all the functions of a normal stack (push, top, pop, and empty).

Implement the MyStack class:

void push(int x) Pushes element x to the top of the stack.
int pop() Removes the element on the top of the stack and returns it.
int top() Returns the element on the top of the stack.
boolean empty() Returns true if the stack is empty, false otherwise.
Notes:

You must use only standard operations of a queue, which means that only push to back, peek/pop from front, size and is empty operations are valid.
Depending on your language, the queue may not be supported natively. You may simulate a queue using a list or deque (double-ended queue) as long as you use only a queue's standard operations.
 
*/
/**
 * Your MyStack object will be instantiated and called as such:
 * MyStack* obj = new MyStack();
 * obj->push(x);
 * int param_2 = obj->pop();
 * int param_3 = obj->top();
 * bool param_4 = obj->empty();
 */
class MyStack {
    queue<int>q1;
    queue<int>q2;
public:
    MyStack() {
        
    }
    
    void push(int x) {
        q1.push(x);
    }
    
    int pop() {
        while(q1.size()!=1){
            q2.push(q1.front());
                q1.pop();
        }
        int x=q1.front();
        q1.pop();
        swap(q1,q2);
        return x;
        
    }
    
    int top() {
        while(q1.size()!=1){
            q2.push(q1.front());
                q1.pop();
        }
        int x=q1.front();
        q1.pop();
        swap(q1,q2);
        q1.push(x);
        return x;
        
    }
  bool empty() {
        return(q1.empty() && q2.empty());
            
    }
};
```
