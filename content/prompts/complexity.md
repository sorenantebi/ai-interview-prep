You are checking the time and space complexity of a candidate's solution to a coding interview problem.

# Problem
{{question}}

# Candidate's code
```python
{{code}}
```

# Candidate's own answer
Time: {{time}}
Space: {{space}}
(If these say "not given", only work out the complexity.)

Work out the time and extra-space complexity of THIS code (not of the best possible solution), using the
problem's input sizes (n, m, k, …). Conventions, as in interviews:
- Time is for the worst-case input, with hash map / set operations counted as O(1).
- Space is the extra memory the code uses, including the recursion stack but not the returned output. If the
  candidate's answer is only right when the output is counted, still mark it correct and say so in "why".
- Accept equivalent answers: constants and lower-order terms dropped (O(2n) = O(n), O(n + n log n) = O(n log n)),
  other variable names if their meaning is clear, and log bases ignored.
- A looser bound (O(n²) for O(n) code) is wrong; so is a tighter one the code doesn't achieve.

Answer with only this JSON, no other text:
{"time": "O(...)", "space": "O(...)", "timeOk": true | false | null, "spaceOk": true | false | null, "why": "one or two short sentences"}
(timeOk / spaceOk are null when the candidate gave no answer.)
