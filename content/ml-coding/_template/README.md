# Adding your own ML coding problem

Folders starting with `_` (like this one) are ignored by the app, so this template never shows up as a topic.

Easiest: **ML Coding → + Add your own** opens these four files in editors, and saves the problem once its tests work.
The steps below are for doing it by hand.

1. Create a folder `ml-coding/<NN Topic>/<problem-name>/` (pick an existing topic like `01 NumPy`, or a new
   name like `06 Transformers` for a new topic).
2. Copy the four files from this folder into it and fill in every `<...>` placeholder:

| File | What it's for |
|---|---|
| `question.md` | The problem page. **Run** reads the `Input:` lines of the examples. |
| `starter.py` | The code you start from: imports plus one function with type hints and `pass`. |
| `solution.md` | Your reference solution in a ```` ```python ```` block. **Run** compares your output with it. |
| `tests.py` | The hidden tests for **Submit**. Only edit `FUNC`, `reference`, `CASES` (and `NUMPY_ONLY`). |

Rules that keep **Run** working:

- One top-level function in `starter.py`, and every parameter has a type hint. `np.ndarray`, `pd.DataFrame`,
  `pd.Series` and `torch.Tensor` arguments are built from the plain lists / dicts written in the examples.
- Example inputs are `name = value` pairs in the order of the parameters, written as Python / JSON literals.
- A DataFrame is written as a dict of columns: `df = {"a": [1, 2], "b": [3, 4]}`.

Check it from the terminal: `node scripts/check-problems.ts "content/ml-coding/<NN Topic>"`.
It runs the examples against your reference, and checks that the reference passes `tests.py` and the empty starter fails it.

Or skip all of this: **AI & Interviews → Generate ML coding problem** writes the four files for you.
