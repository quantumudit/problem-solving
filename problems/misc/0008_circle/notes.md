# Dunder Methods (Magic Methods) - Circle Class

## What are Dunder Methods?

Dunder methods (double underscore methods) are special methods in Python that allow you to define how objects behave with built-in operations and functions. They have names surrounded by double underscores (e.g., `__repr__`, `__add__`).

---

## Dunder Methods in Circle Class

### 1. `__repr__()` - String Representation

Returns a string representation of the object. Useful for debugging and logging.

```python
def __repr__(self):
    return f"Circle(radius={self.radius})"
```

**Usage:**
```python
c = Circle(5.0)
print(c)                    # Output: Circle(radius=5.0)
print(repr(c))              # Output: Circle(radius=5.0)
```

---

### 2. `__eq__()` - Equality Comparison

Compares two objects. Returns `True` if both circles have the same radius.

```python
def __eq__(self, other):
    if not isinstance(other, Circle):
        return False
    return self.radius == other.radius
```

**Usage:**
```python
c1 = Circle(5.0)
c2 = Circle(5.0)
c3 = Circle(3.0)

print(c1 == c2)             # Output: True
print(c1 == c3)             # Output: False
if c1 == c2:
    print("Same circles!")  # This will print
```

---

### 3. `__lt__()` - Less-Than Comparison

Compares objects by area. Enables sorting and use with `min()`, `max()`.

```python
def __lt__(self, other):
    if not isinstance(other, Circle):
        return NotImplemented
    return self.area < other.area
```

**Usage:**
```python
c1 = Circle(2.0)
c2 = Circle(5.0)
c3 = Circle(3.0)

print(c1 < c2)              # Output: True (smaller area)
circles = [c2, c1, c3]
sorted_circles = sorted(circles)  # Sorts by area
print([c.radius for c in sorted_circles])  # Output: [2.0, 3.0, 5.0]

smallest = min(circles)     # Returns c1 (smallest area)
largest = max(circles)      # Returns c2 (largest area)
```

---

### 4. `__add__()` - Addition Operator

Returns a new Circle whose radius is the sum of both radii.

```python
def __add__(self, other):
    if not isinstance(other, Circle):
        return NotImplemented
    return Circle(self.radius + other.radius)
```

**Usage:**
```python
c1 = Circle(3.0)
c2 = Circle(4.0)

c3 = c1 + c2                # Creates Circle(radius=7.0)
print(c3)                   # Output: Circle(radius=7.0)
print(c3.area)              # Area of combined circle
```

---

## Benefits of Dunder Methods

1. **Intuitive API** - Objects behave like built-in types
2. **Sortable** - Implement `__lt__` and `__eq__` to sort objects
3. **Comparable** - Use objects in comparisons (`<`, `>`, `==`)
4. **Operable** - Support operators like `+`, `-`, etc.
5. **Readable** - Makes code more Pythonic and expressive

---

## Input Validation

The Circle class validates input to prevent invalid states:

```python
def __init__(self, radius: float):
    if radius < 0:
        raise ValueError("Radius cannot be negative")
    self.radius = radius
```

**Usage:**
```python
c = Circle(-5.0)  # Raises ValueError: Radius cannot be negative
```

---

## Complete Example

```python
from math import pi

class Circle:
    def __init__(self, radius: float):
        if radius < 0:
            raise ValueError("Radius cannot be negative")
        self.radius = radius
        self.area = pi * self.radius ** 2
    
    def __repr__(self):
        return f"Circle(radius={self.radius})"
    
    def __eq__(self, other):
        if not isinstance(other, Circle):
            return False
        return self.radius == other.radius
    
    def __lt__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return self.area < other.area
    
    def __add__(self, other):
        if not isinstance(other, Circle):
            return NotImplemented
        return Circle(self.radius + other.radius)

# Create circles
circles = [Circle(5), Circle(2), Circle(8), Circle(3)]

# Sort by area
sorted_circles = sorted(circles)
print([c.radius for c in sorted_circles])  # [2, 3, 5, 8]

# Find extremes
print(min(circles))  # Circle(radius=2)
print(max(circles))  # Circle(radius=8)

# Add circles
result = Circle(3) + Circle(4)
print(result)  # Circle(radius=7)

# Compare
print(Circle(5) == Circle(5))  # True
print(Circle(2) < Circle(5))   # True (smaller area)
```
