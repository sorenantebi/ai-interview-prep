"""wordgame: small helpers for a letter-based word puzzle.

The package turns words into letter bitmasks, cleans raw user input and
computes the best selection of words that never reuse a letter.
"""

from .report import format_summary, summarize_text
from .solver import max_unique_length

__all__ = ["format_summary", "summarize_text", "max_unique_length"]
