"""R's formulate(): turn an equation string into a callable with one argument per
basic event. The equation is parsed by a small +/*/() grammar -- never eval()."""

from __future__ import annotations

import inspect
import keyword
import re

import numpy as np

_IDENT = re.compile(r"^[a-zA-Z][a-zA-Z0-9_.]*$")
_TOKEN = re.compile(r"\s*(?:(?P<name>[A-Za-z][A-Za-z0-9_.]*)|(?P<num>\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)|(?P<op>[()+*]))")


def r_sort(values):
    """Order strings the way R's sort() does under an English locale: letters
    compared case-insensitively, lowercase first on ties, punctuation and digits
    before letters. Exact for the names fault trees use (letters, digits, _ .)."""
    return sorted(values, key=lambda s: (s.lower(), s.swapcase()))


def _tokens(text):
    pos, out = 0, []
    text = text.rstrip()
    while pos < len(text):
        m = _TOKEN.match(text, pos)
        if not m or m.end() == pos:
            raise ValueError(f"formulate(): cannot parse {text[pos:].strip()[:20]!r} in the equation; "
                             "only event names, numbers, +, * and parentheses are allowed")
        kind = m.lastgroup
        out.append((kind, m.group(kind)))
        pos = m.end()
    return out


class _Parser:
    def __init__(self, toks):
        self.t, self.i = toks, 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def take(self):
        tok = self.peek()
        self.i += 1
        return tok

    def expr(self):
        node = self.term()
        while self.peek() == ("op", "+"):
            self.take()
            node = ("+", node, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.peek() == ("op", "*"):
            self.take()
            node = ("*", node, self.factor())
        return node

    def factor(self):
        kind, val = self.take()
        if kind == "name":
            return ("name", val)
        if kind == "num":
            return ("num", float(val), val)
        if (kind, val) == ("op", "("):
            inner = self.expr()
            if self.take() != ("op", ")"):
                raise ValueError("formulate(): unbalanced parentheses in the equation")
            return ("paren", inner)
        raise ValueError(f"formulate(): unexpected {val!r} in the equation")


def _parse(formula):
    p = _Parser(_tokens(formula))
    tree = p.expr()
    if p.i != len(p.t):
        raise ValueError(f"formulate(): unexpected {p.peek()[1]!r} in the equation")
    return tree


def _eval(node, env):
    kind = node[0]
    if kind == "name":
        return env[node[1]]
    if kind == "num":
        return node[1]
    if kind == "paren":
        return _eval(node[1], env)
    a, b = _eval(node[1], env), _eval(node[2], env)
    return a + b if kind == "+" else a * b


def _deparse(node):
    kind = node[0]
    if kind == "name":
        return node[1]
    if kind == "num":
        return node[2]
    if kind == "paren":
        return "(" + _deparse(node[1]) + ")"
    return _deparse(node[1]) + f" {kind} " + _deparse(node[2])


class Formula:
    """What formulate() returns: call it like R's function, positionally in
    ``args`` order or by name, with 0/1 (or any numeric) scalars or arrays.
    ``repr()`` prints like R prints the function."""

    def __init__(self, formula):
        self.formula = formula
        self._tree = _parse(formula)
        values = [v.strip() for v in re.split(r"[()*+]", formula)]
        values = [v for v in values if v and _IDENT.match(v)]
        self.args = r_sort(list(dict.fromkeys(values)))
        self.body = _deparse(self._tree)
        if all(a.isidentifier() and not keyword.iskeyword(a) for a in self.args):
            self.__signature__ = inspect.Signature(
                [inspect.Parameter(a, inspect.Parameter.POSITIONAL_OR_KEYWORD) for a in self.args])

    def __call__(self, *args, **kwargs):
        if len(args) > len(self.args):
            raise TypeError(f"unused argument(s): {len(args) - len(self.args)} extra positional value(s)")
        env = dict(zip(self.args, args))
        for k, v in kwargs.items():
            if k not in self.args:
                raise TypeError(f"unused argument ({k} = ...)")
            if k in env:
                raise TypeError(f"formal argument \"{k}\" matched by multiple actual arguments")
            env[k] = v
        missing = [a for a in self.args if a not in env]
        if missing:
            raise TypeError(f'argument "{missing[0]}" is missing, with no default')
        env = {k: (np.asarray(v, dtype=float) if np.ndim(v) else float(v)) for k, v in env.items()}
        return _eval(self._tree, env)

    def __repr__(self):
        return f"function ({', '.join(self.args)}) \n{self.body}"


def formulate(formula) -> Formula:
    """Equation string (from equate()) -> callable with one argument per basic
    event, sorted like R's ``sort()``; ``*`` is AND and ``+`` is OR, evaluated as
    arithmetic exactly as R does (so a failure can evaluate to 2, 3, ...)."""
    return Formula(formula)


def formal_args(f):
    """R's ``formalArgs(f)``: argument names of a formulate() result or any function."""
    if isinstance(f, Formula):
        return list(f.args)
    return list(inspect.signature(f).parameters)
