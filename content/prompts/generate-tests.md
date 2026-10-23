Write a Python 3 test file `tests.py` for the problem below. The user's solution lives in `attempt.py` next to it.

Rules:
- Do NOT `import attempt`. Load it like this so type hints that use ListNode/TreeNode work:
  ```python
  ns = {"ListNode": ListNode, "TreeNode": TreeNode, "List": List, "Optional": Optional, "Dict": Dict}
  exec(open("attempt.py").read(), ns)
  ```
  Define `ListNode`, `TreeNode` (LeetCode's definitions) and list/tree build/serialize helpers in tests.py before that.
- Use the method signature from the reference solution. For design problems (class with operations), replay operation sequences.
- 8-15 cases: all examples from the question plus edge cases (empty, single element, duplicates, negatives, large input for performance when relevant).
- When order does not matter (e.g. groups, permutations), compare in a canonical (sorted) form.
- For each case print `PASS case N` or `FAIL case N: input=..., expected=..., got=...`. A raised exception counts as FAIL with the error message.
- End with a summary line `X/Y passed` and `sys.exit(1)` if any failed.
- Standard library only.

Answer with only the file:

=== FILE: tests.py ===
<code>
=== END ===

# Question
{{question}}

# Reference solution
{{solution}}
