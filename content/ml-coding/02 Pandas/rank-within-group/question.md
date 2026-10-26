---
topic: "Pandas"
difficulty: Medium
---
# Rank Within Group

**Topic:** Pandas · **Difficulty:** Medium

## Problem

You get a DataFrame `df` of employees with columns `dept`, `name` and `salary`.

Return a copy of `df` with an extra integer column `rank` at the end: the employee's salary rank inside their department, where `1` is the highest salary. Employees with the same salary in a department share a rank, and the next lower salary gets the next rank with no gaps (so salaries 9, 9, 7 get ranks 1, 1, 2). Keep the original row order and index, and don't modify `df`.

## Examples

**Example 1**
```text
Input: df = {"dept": ["eng", "eng", "ops", "eng"], "name": ["a", "b", "c", "d"], "salary": [100, 120, 90, 100]}
Output: {"dept":["eng","eng","ops","eng"],"name":["a","b","c","d"],"salary":[100,120,90,100],"rank":[2,1,1,2]}
Explanation: in eng, b earns most (rank 1) and a and d tie (rank 2).
```

**Example 2**
```text
Input: df = {"dept": ["x", "x", "x"], "name": ["p", "q", "r"], "salary": [9, 9, 7]}
Output: {"dept":["x","x","x"],"name":["p","q","r"],"salary":[9,9,7],"rank":[1,1,2]}
```

## Constraints

- `0 <= len(df) <= 10^5`
- `salary` has no missing values
