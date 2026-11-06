"""Turn formula text into a flat list of tokens."""

from dataclasses import dataclass

from .errors import TokenError

OPERATORS = "+-*/"

# Token kinds that may precede a '-' sign which starts a negative literal.
_SIGN_CONTEXT = (None, "LPAREN", "COMMA")


@dataclass(frozen=True)
class Token:
    """A lexical token: NUMBER, REF, FUNC, OP, LPAREN, RPAREN, COMMA or END."""

    kind: str
    value: object
    pos: int


def tokenize(text):
    """Split ``text`` into a list of tokens, always ending with an END token."""
    tokens = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            i += 1
        elif ch.isdigit() or ch == "." or (ch == "-" and _starts_negative(text, i, tokens)):
            i = _read_number(text, i, tokens)
        elif ch.isalpha():
            i = _read_name(text, i, tokens)
        elif ch in OPERATORS:
            tokens.append(Token("OP", ch, i))
            i += 1
        elif ch == "(":
            tokens.append(Token("LPAREN", ch, i))
            i += 1
        elif ch == ")":
            tokens.append(Token("RPAREN", ch, i))
            i += 1
        elif ch == ",":
            tokens.append(Token("COMMA", ch, i))
            i += 1
        else:
            raise TokenError(f"unexpected character {ch!r} at position {i}")
    tokens.append(Token("END", None, n))
    return tokens


def _starts_negative(text, i, tokens):
    """True if the '-' at ``i`` is the sign of a number rather than subtraction."""
    prev = tokens[-1].kind if tokens else None
    nxt = text[i + 1] if i + 1 < len(text) else ""
    return prev in _SIGN_CONTEXT and (nxt.isdigit() or nxt == ".")


def _read_number(text, i, tokens):
    start = i
    if text[i] == "-":
        i += 1
    seen_dot = False
    while i < len(text) and (text[i].isdigit() or text[i] == "."):
        if text[i] == ".":
            if seen_dot:
                raise TokenError(f"malformed number at position {start}")
            seen_dot = True
        i += 1
    raw = text[start:i]
    try:
        value = float(raw)
    except ValueError:
        raise TokenError(f"malformed number {raw!r} at position {start}") from None
    tokens.append(Token("NUMBER", value, start))
    return i


def _read_name(text, i, tokens):
    start = i
    while i < len(text) and text[i].isalnum():
        i += 1
    word = text[start:i]
    if i < len(text) and text[i] == "(":
        tokens.append(Token("FUNC", word.upper(), start))
    else:
        tokens.append(Token("REF", word, start))
    return i
