"""Evaluate parsed formula trees."""

from .errors import EvalError
from .parser import BinOp, Call, Number, Ref


def _minimum(values):
    if not values:
        raise EvalError("MIN needs at least one argument")
    return min(values)


def _maximum(values):
    if not values:
        raise EvalError("MAX needs at least one argument")
    return max(values)


def _average(values):
    if not values:
        raise EvalError("AVG needs at least one argument")
    return sum(values) / len(values)


FUNCTIONS = {
    "SUM": lambda values: float(sum(values)),
    "MIN": _minimum,
    "MAX": _maximum,
    "AVG": _average,
}


class Evaluator:
    """Evaluates expression trees; cell values come from the ``resolve`` callback."""

    def __init__(self, resolve):
        self._resolve = resolve

    def evaluate(self, node):
        if isinstance(node, Number):
            return node.value
        if isinstance(node, Ref):
            return self._resolve(node.name)
        if isinstance(node, BinOp):
            return self._binary(node)
        if isinstance(node, Call):
            return self._call(node)
        raise EvalError(f"cannot evaluate node {node!r}")

    def _binary(self, node):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        if node.op == "+":
            return left + right
        if node.op == "-":
            return left - right
        if node.op == "*":
            return left * right
        if node.op == "/":
            if right == 0:
                raise EvalError("division by zero")
            return left / right
        raise EvalError(f"unknown operator {node.op!r}")

    def _call(self, node):
        func = FUNCTIONS.get(node.name)
        if func is None:
            raise EvalError(f"unknown function {node.name}")
        return func([self.evaluate(arg) for arg in node.args])
