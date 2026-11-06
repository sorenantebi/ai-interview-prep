"""Exception types raised by the formula package."""


class FormulaError(Exception):
    """Base class for every error raised while processing a formula."""


class TokenError(FormulaError):
    """The formula text contains something that is not a valid token."""


class ParseError(FormulaError):
    """The tokens do not form a valid expression."""


class EvalError(FormulaError):
    """A valid expression could not be evaluated (division by zero, cycles...)."""
