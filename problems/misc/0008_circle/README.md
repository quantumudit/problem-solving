---
platform: misc
problem_id: "0008"
slug: circle
difficulty: null
link: ""
dataset: none
---

# Circle

A Python class that represents a circle and exposes a full set of
geometric properties, transformation methods, and comparison operators,
with a Rich-formatted display method.

## Class Interface

### Constructor

```python
Circle(radius: float)
```

Raise ValueError if radius is negative.

### Properties (read-only)

| Property      | Formula                      | Description                   |
|---------------|------------------------------|-------------------------------|
| diameter      | 2 * r                        | Full width across the circle  |
| area          | pi * r^2                     | Enclosed area                 |
| circumference | 2 * pi * r                   | Perimeter of the circle       |

Use math.pi for all calculations. Round displayed values to 4 decimal
places in output, but store the full float internally.

### Methods

| Method                   | Description                                       |
|--------------------------|---------------------------------------------------|
| sector_area(angle_deg)   | Area of a sector with the given central angle     |
| arc_length(angle_deg)    | Arc length for the given central angle            |
| is_unit_circle()         | Return True if radius == 1.0                      |
| scale(factor)            | Return a new Circle with radius * factor          |
| display()                | Print a Rich panel showing all properties         |

Formulas:
- sector_area(angle) = (angle / 360) * pi * r^2
- arc_length(angle)  = (angle / 360) * 2 * pi * r

Raise ValueError in sector_area and arc_length if angle is not in
the range (0, 360] inclusive.

### Dunder Methods

| Dunder     | Behavior                                            |
|------------|-----------------------------------------------------|
| __repr__   | Circle(radius=5.0)                                  |
| __eq__     | True if both circles have the same radius           |
| __lt__     | Compare by area (smaller area is less-than)         |
| __add__    | Return a new Circle whose radius is the sum of both |

Implementing __lt__ and __eq__ makes the class sortable and usable
with min(), max(), and sorted().

## Example Usage

```python
c1 = Circle(5)
c2 = Circle(3)

c1.area            # 78.5398...
c1.circumference   # 31.4159...
c1.diameter        # 10.0
c1.sector_area(90) # 19.6349...
c1.arc_length(90)  # 7.8539...

c1 > c2            # True
c1 + c2            # Circle(radius=8.0)
c1.scale(0.5)      # Circle(radius=2.5)

sorted([c1, c2])   # [Circle(radius=3.0), Circle(radius=5.0)]
```

## CLI Interface

A `demo` command that creates a Circle from a user-supplied radius,
then calls display() to render all properties in a Rich panel.

```
python solution.py demo 5
python solution.py demo 3.14
```
