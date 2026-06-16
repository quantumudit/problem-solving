from math import pi

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# -------------------------------------------------------
# Circle Class
# -------------------------------------------------------

class Circle:
    def __init__(self, radius: float):
        if radius < 0:
            raise ValueError("Radius cannot be negative.")
        self.radius = float(radius)

    # -- read-only properties --

    @property
    def diameter(self) -> float:
        return 2 * self.radius

    @property
    def area(self) -> float:
        return pi * self.radius ** 2

    @property
    def circumference(self) -> float:
        return 2 * pi * self.radius

    # -- methods --

    def sector_area(self, angle: float) -> float:
        if not 0 < angle <= 360:
            raise ValueError("Angle must be in the range (0, 360] inclusive.")
        return (angle / 360) * self.area

    def arc_length(self, angle: float) -> float:
        if not 0 < angle <= 360:
            raise ValueError("Angle must be in the range (0, 360] inclusive.")
        return (angle / 360) * self.circumference

    def is_unit_circle(self) -> bool:
        return self.radius == 1.0

    def scale(self, factor: float) -> "Circle":
        return Circle(self.radius * factor)

    def display(self) -> None:
        table = Table(show_header=True, header_style="bold cyan", show_lines=True)
        table.add_column("Property",      style="bold")
        table.add_column("Value",         justify="right")
        table.add_row("Radius",        f"{self.radius:.4f}")
        table.add_row("Diameter",      f"{self.diameter:.4f}")
        table.add_row("Area",          f"{self.area:.4f}")
        table.add_row("Circumference", f"{self.circumference:.4f}")
        console.print(Panel(table, title=repr(self), border_style="cyan"))

    # -- dunder methods --

    def __repr__(self) -> str:
        return f"Circle(radius={self.radius})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Circle):
            return False
        return self.radius == other.radius

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Circle):
            return NotImplemented  # type: ignore[return-value]
        return self.area < other.area

    def __add__(self, other: object) -> "Circle":
        if not isinstance(other, Circle):
            return NotImplemented  # type: ignore[return-value]
        return Circle(self.radius + other.radius)
