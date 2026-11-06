"""Recursive-descent parser producing a small expression tree."""

from dataclasses import dataclass

from .errors import ParseError
from .tokenizer import tokenize


@dataclass(frozen=True)
class Number:
    value: float


@dataclass(frozen=True)
class Ref:
    name: str


@dataclass(frozen=True)
class BinOp:
    op: str
    left: object
    right: object


@dataclass(frozen=True)
class Call:
    name: str
    args: tuple


class Parser:
    """Parses a token list.

    Grammar::

        expression := term (('+' | '-') term)*
        term       := factor (('*' | '/') factor)*
        factor     := NUMBER | REF | FUNC '(' [expression (',' expression)*] ')'
                    | '(' expression ')'
    """

    def __init__(self, tokens):
        self._tokens = tokens
        self._pos = 0

    def _peek(self):
        return self._tokens[self._pos]

    def _advance(self):
        tok = self._tokens[self._pos]
        self._pos += 1
        return tok

    def _match_op(self, *ops):
        tok = self._peek()
        if tok.kind == "OP" and tok.value in ops:
            return self._advance()
        return None

    def _expect(self, kind):
        tok = self._peek()
        if tok.kind != kind:
            raise ParseError(f"expected {kind} at position {tok.pos}")
        return self._advance()

    def parse(self):
        node = self.parse_expression()
        tok = self._peek()
        if tok.kind != "END":
            raise ParseError(f"unexpected token {tok.value!r} at position {tok.pos}")
        return node

    def parse_expression(self):
        node = self.parse_term()
        while True:
            op = self._match_op("+", "-")
            if op is None:
                return node
            node = BinOp(op.value, node, self.parse_term())

    def parse_term(self):
        node = self.parse_factor()
        while True:
            op = self._match_op("*", "/")
            if op is None:
                return node
            node = BinOp(op.value, node, self.parse_factor())

    def parse_factor(self):
        tok = self._advance()
        if tok.kind == "NUMBER":
            return Number(tok.value)
        if tok.kind == "REF":
            return Ref(tok.value)
        if tok.kind == "FUNC":
            return self._parse_call(tok)
        if tok.kind == "LPAREN":
            node = self.parse_expression()
            self._expect("RPAREN")
            return node
        if tok.kind == "END":
            raise ParseError("unexpected end of formula")
        raise ParseError(f"unexpected token {tok.value!r} at position {tok.pos}")

    def _parse_call(self, tok):
        self._expect("LPAREN")
        args = []
        if self._peek().kind != "RPAREN":
            args.append(self.parse_expression())
            while self._peek().kind == "COMMA":
                self._advance()
                args.append(self.parse_expression())
        self._expect("RPAREN")
        return Call(tok.value, tuple(args))


def parse(text):
    """Parse formula text (without a leading '=') into an expression tree."""
    return Parser(tokenize(text)).parse()
