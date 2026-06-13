---
platform: misc
problem_id: "0003"
slug: calculator
difficulty: null
difficulty_rating: easy
language: [python]
topics: [string_ops, conditional_logic]
date_solved: 2026-06-14
revisit: false
---

# Notes

## `eval()` -- Evaluating a String as a Python Expression

`eval()` takes a string and executes it as a Python expression, returning the result.

```python
eval("2 + 3")        # 5
eval("10 / 4")       # 2.5
eval("2 ** 8")       # 256
```

It is essentially Python reading and running a piece of code at runtime. Useful for
calculators and expression parsers, but dangerous by default because it runs with
full access to Python's built-in functions and the calling scope.

```python
eval("__import__('os').system('dir')")  # runs a shell command -- dangerous
```

---

## Restricting `eval()` with a Namespace

`eval()` accepts two optional arguments that control what names are accessible
during evaluation:

```python
eval(expression, globals_dict, locals_dict)
```

- `globals_dict` -- what is available as global names inside the expression
- `locals_dict` -- what is available as local names inside the expression

By passing custom dicts you replace the default scope entirely:

```python
eval("2 + 3", {}, {})   # works -- no names needed, just literals and operators
eval("x + 1", {}, {})   # NameError: name 'x' is not defined
```

---

## Stripping Built-ins with `{"__builtins__": {}}`

Even with empty dicts, Python injects `__builtins__` into the globals unless you
explicitly override it. `__builtins__` is what gives expressions access to `open()`,
`__import__()`, `exec()`, and everything else in the standard built-in namespace.

Passing `{"__builtins__": {}}` as globals removes that injection entirely:

```python
eval("open('file.txt')", {"__builtins__": {}}, {})
# NameError: name 'open' is not defined
```

Now the expression runs in a fully locked-down environment with no access to any
built-in function.

---

## Allowing Specific Names

To allow certain functions back in, add them to the locals dict by name. The dict
maps the string name (as it will appear in the expression) to the actual callable:

```python
import math

allowed_names = {
    "sqrt":  math.sqrt,
    "abs":   abs,
    "round": round,
}

eval("sqrt(144)", {"__builtins__": {}}, allowed_names)   # 12.0
eval("abs(-7)",   {"__builtins__": {}}, allowed_names)   # 7
eval("open('x')", {"__builtins__": {}}, allowed_names)   # NameError -- blocked
```

The key in the dict is the name that appears in the expression string. The value is
whatever Python object that name should resolve to -- it does not have to match the
original function name:

```python
allowed_names = {"root": math.sqrt}
eval("root(9)", {"__builtins__": {}}, allowed_names)   # 3.0
```

---

## Regex as the First Line of Defense

`eval()` with a restricted namespace stops execution-time attacks (e.g. `__import__`
raising `NameError`). But the expression still gets parsed by Python before any
`NameError` is raised, which means carefully crafted strings could exploit the parser
itself.

Regex validation before `eval()` adds a structural gate -- reject any expression
that contains characters outside the known-safe set before it ever reaches the
interpreter:

```python
import re

_ALLOWED = re.compile(r"^(sqrt|abs|round|[\d\s+\-*/%().])+$")

if not _ALLOWED.match(expression):
    return "Error: expression contains disallowed characters"
```

The two layers together -- regex rejects unknown structure, restricted namespace
blocks unknown names -- make `eval()` safe for a trusted input surface like a REPL.
