---
topic: "NumPy Basics"
difficulty: Easy
---
# Celsius to Fahrenheit

**Topic:** NumPy Basics · **Difficulty:** Easy

## Problem

Write `celsius_to_fahrenheit(celsius)`, which receives a NumPy array `celsius` of temperatures in degrees Celsius (any shape, dtype `float64` or `int64`) and returns a new array of the same shape with each temperature converted to degrees Fahrenheit and rounded to 1 decimal place.

Use the formula `F = C * 9 / 5 + 32`.

Calls to practise: vectorised arithmetic (`*`, `/`, `+` applied to the whole array at once) and `np.round`. Don't use Python loops or list comprehensions, and don't modify the input array.

**Rules:** build it from basic NumPy: array creation, indexing (including fancy indexing with index arrays), reshape / transpose, broadcasting, arithmetic, reductions (`sum`, `max`, `mean`, …), `np.sort` / `np.argsort` and `@`. Not allowed: `np.einsum`, `np.tensordot`, `np.convolve`, `np.correlate`, `np.linalg.norm`, `sliding_window_view` / `as_strided`, and other libraries (SciPy, scikit-learn, pandas, PyTorch). The hidden tests reject them.

## Examples

**Example 1**
```text
Input: celsius = [0.0, 100.0, -40.0, 37.0]
Output: [32.00000,212.00000,-40.00000,98.60000]
Explanation: Water freezes at 32 °F and boils at 212 °F; -40 is the same in both scales.
```

**Example 2**
```text
Input: celsius = [[20.5, 25.3], [-10.0, 36.6]]
Output: [[68.90000,77.50000],[14.00000,97.90000]]
Explanation: 25.3 * 9 / 5 + 32 = 77.54, which rounds to 77.5; 36.6 gives 97.88, which rounds to 97.9.
```

**Example 3**
```text
Input: celsius = [[-273.15]]
Output: [[-459.70000]]
Explanation: Absolute zero is -459.67 °F, rounded to 1 decimal.
```

## Constraints

- `1 <= celsius.size <= 10^6`
- `-300 <= celsius[i] <= 1000`
