import math
import re
from typing import Literal

# -------------------------------------------------------
# Calculator Class
# -------------------------------------------------------

_ALLOWED_EXPR = re.compile(r"^(sqrt|abs|round|[\d\s+\-*/%().])+$")

_ALLOWED_NAMES: dict[str, object] = {
    "sqrt": math.sqrt,
    "abs":  abs,
    "round": round,
}

_MANUAL_OPS: dict[str, object] = {
    "+":  lambda a, b: a + b,
    "-":  lambda a, b: a - b,
    "*":  lambda a, b: a * b,
    "/":  lambda a, b: a / b,
    "%":  lambda a, b: a % b,
    "**": lambda a, b: a ** b,
}


class Calculator:
    def __init__(self, mode: Literal["expression", "manual"]):
        self.mode = mode
        self.history: list[str] = []

    def evaluate(self, expression: str) -> str:
        if not _ALLOWED_EXPR.match(expression):
            return "Error: expression contains disallowed characters"
        try:
            result = eval(expression, {"__builtins__": {}}, _ALLOWED_NAMES)
        except ZeroDivisionError:
            return "Error: division by zero"
        except (SyntaxError, NameError, TypeError, ValueError) as e:
            return f"Error: {e}"
        self.history.append(f"{expression} = {result}")
        return str(result)

    def compute(self, a: int | float, b: int | float, operator: str) -> str:
        if operator not in _MANUAL_OPS:
            return f"Error: unsupported operator '{operator}'"
        if operator in ("/", "%") and b == 0:
            return "Error: division by zero"
        result = _MANUAL_OPS[operator](a, b)
        self.history.append(f"{a} {operator} {b} = {result}")
        return str(result)

    def get_history(self) -> list[str]:
        return self.history

    def clear_history(self) -> None:
        self.history = []
