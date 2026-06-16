from math import pi

class Circle:
    def __init__(self, radius: float):
        if radius < 0:
            raise ValueError("Radius cannot be negative")
        self.radius = radius
        self.diameter = 2 * radius
        self.circumference = 2 * pi * radius
        self.area = pi * self.radius ** 2
    
    def sector_area(self, angle: float):
        if angle in range(0, 361):
            return (angle / 360) * self.area
        raise ValueError("Angle must be in the range (0, 360] inclusive")
    
    def arc_length(self, angle: float):
        if angle in range(0, 361):
            return (angle / 360) * self.circumference
        raise ValueError("Angle must be in the range (0, 360] inclusive")

    def is_unit_circle(self):
        if self.radius == 1:
            return True
        return False
    
    def scale(self, factor):
        return Circle(self.radius * factor)
    
    def display(self):
        print(f"Circle Properties:")
        print(f"  Radius: {self.radius}")
        print(f"  Diameter: {self.diameter}")
        print(f"  Circumference: {self.circumference:.2f}")
        print(f"  Area: {self.area:.2f}")
    
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
