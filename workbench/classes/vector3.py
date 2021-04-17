class Vector3(object):
    def __init__(self, x: float, y: float, z: float):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self):  # for debugging
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def __str__(self):  # for printing
        return f"{self.x}, {self.y}, {self.z}"

    def __eq__(self, other):
        """Overload equality operator."""
        if not isinstance(other, Vector3):
            return False
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __add__(self, other):
        """Overload addition operator."""
        if isinstance(other, Vector3):
            x = self.x + other.x
            y = self.y + other.y
            z = self.z + other.z
        else:
            x = self.x + other
            y = self.y + other
            z = self.z + other
        return Vector3(x, y, z)

    def __sub__(self, other):
        """Overload subtraction operator."""
        if isinstance(other, Vector3):
            x = self.x - other.x
            y = self.y - other.y
            z = self.z - other.z
        else:
            x = self.x - other
            y = self.y - other
            z = self.z - other
        return Vector3(x, y, z)

    def __mul__(self, other):
        """Overload multiplication operator."""
        if isinstance(other, Vector3):
            x = self.x * other.x
            y = self.y * other.y
            z = self.z * other.z
        else:
            x = self.x * other
            y = self.y * other
            z = self.z * other
        return Vector3(x, y, z)

    def __truediv__(self, other):
        """Overload division operator."""
        if isinstance(other, Vector3):
            x = self.x / other.x
            y = self.y / other.y
            z = self.z / other.z
        else:
            x = self.x / other
            y = self.y / other
            z = self.z / other
        return Vector3(x, y, z)

    def magnitude(self):
        """Compute magnitude (length)."""
        x = self.x**2
        y = self.y**2
        z = self.z**2
        return sqrt(x + y + z)
