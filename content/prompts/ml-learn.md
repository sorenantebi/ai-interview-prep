You are writing the "learn" page for one practice problem in the ML coding section of a study app. The reader has
opened the problem and doesn't yet know how to solve it: they may never have used this library function or met this
ML idea. After reading your page they should understand the idea well enough to write the solution themselves.
Teach; don't solve.

Topic: {{topic}}

The problem, as the reader sees it:
<question>
{{question}}
</question>

The reference solution (for you only; the reader can open it in the Solution tab, so never copy it):
<solution>
{{solution}}
</solution>

Write the page in Markdown with exactly these sections, in this order. Everything is bullet points, not paragraphs:
one short idea per bullet (one sentence, two at most), nested bullets for detail, `**bold**` for the term a bullet
defines. The only exceptions are the ```python demos and an optional table in "Work it by hand".

# Learn: <the problem's title>

## The idea
Bullets: what the task is really asking, in plain words; where it shows up in ML or data work (a training loop, a
feature pipeline, an evaluation report, ...); one bullet per term a beginner might not know (e.g. "broadcasting",
"logits", "bias correction", "groupby"), defining it. For an ML concept, the intuition bullets come before the formula.

## Work it by hand
Take Example 1 from the question and walk through it step by step on paper: the intermediate values and shapes after
each step, ending at the exact expected output. Keep the same numbers as the question. A numbered list (one step per
item) or a small table. This is the part that makes the idea click, so don't skip steps.

## Tools you'll need
Every library function, method, operator or language feature the solution relies on, plus any the reader will
probably reach for, one `###` subsection each (e.g. `### np.where(cond, a, b)`):
- 1-3 bullets on what it does and the arguments that matter here (axis, keepdims, dtype, inplace, ...);
- a tiny demo in a ```python block on DIFFERENT, made-up data (not the problem's inputs, and not a piece of the
  solution), with the printed result written as a comment under each print, e.g. `print(a.sum(axis=0))  # [4 6]`.
Shapes are where beginners get lost: when a tool changes a shape, print `.shape` too.

## Common mistakes
3-5 bullets: the specific traps in this problem (wrong axis, integer division, modifying the input in place,
off-by-one, NaN handling, forgetting `keepdims`, returning a tensor that still tracks gradients, ...), each with how
to avoid it.

## Hints
Three hints, each a `###` heading, from gentle to nearly complete. The reader opens them one at a time.
### Hint 1
The plan in words, one bullet per step, in order. No code.
### Hint 2
One bullet per step: which tool solves it, and the shape of the data after it. At most a single short expression in
inline code.
### Hint 3
Bullets that spell out the trickiest step in plain words (the formula or the indexing in words or maths), so that
only typing the code is left. Still no code block.

Rules:
- Every ```python block is a complete, runnable snippet on its own: it has its own imports (`import numpy as np`,
  `import pandas as pd`, `import torch`) and needs nothing else. The app runs every block and rejects the page if any
  block fails, and the printed values in your comments must be what the code really prints. Keep each block short
  (2-8 lines). Use ```text for anything that isn't runnable Python.
- Never include the solution's code or a line from it, and no block that solves the problem (or a near copy of it on
  other data). The reader must still write the function.
- Plain, friendly English, short bullets, no filler ("In this problem we will..."). Explain with concrete
  numbers rather than abstractions. Use maths only where it helps, written in plain text or inline code (no LaTeX).
- Stick to what this problem needs. About 400-900 words in total.
- Reply with the Markdown page only, nothing before or after it.
{{rewrite}}