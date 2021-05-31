class Quaternion(object):
    def __init__(self, w: float, x: float, y: float, z: float):
        self.w = float(w)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self):  # for debugging
        return f"Quaternion({self.w}, {self.x}, {self.y}, {self.z})"

    def __str__(self):  # for printing
        return f"{self.w}, {self.x}, {self.y}, {self.z}"

    def __eq__(self, other):
        """Overload equality operator."""
        if not isinstance(other, Quaternion):
            return False
        return (self.w == other.w) and (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __add__(self, other):
        """Overload addition operator."""
        if isinstance(other, Quaternion):
            w = self.w + other.w
            x = self.x + other.x
            y = self.y + other.y
            z = self.z + other.z
        else:
            w = self.w + other
            x = self.x + other
            y = self.y + other
            z = self.z + other
        return Quaternion(w, x, y, z)

    def __sub__(self, other):
        """Overload subtraction operator."""
        if isinstance(other, Quaternion):
            w = self.w - other.w
            x = self.x - other.x
            y = self.y - other.y
            z = self.z - other.z
        else:
            w = self.w - other
            x = self.x - other
            y = self.y - other
            z = self.z - other
        return Quaternion(w, x, y, z)

    def __mul__(self, other):
        """Overload multiplication operator."""
        if isinstance(other, Quaternion):
            w = self.w * other.w
            x = self.x * other.x
            y = self.y * other.y
            z = self.z * other.z
        else:
            w = self.w * other
            x = self.x * other
            y = self.y * other
            z = self.z * other
        return Quaternion(w, x, y, z)

    def __truediv__(self, other):
        """Overload division operator."""
        if isinstance(other, Quaternion):
            w = self.w / other.w
            x = self.x / other.x
            y = self.y / other.y
            z = self.z / other.z
        else:
            w = self.w / other
            x = self.x / other
            y = self.y / other
            z = self.z / other
        return Quaternion(w, x, y, z)

    def magnitude(self):
        """Compute magnitude (length)."""
        w = self.w**2
        x = self.x**2
        y = self.y**2
        z = self.z**2
        return sqrt(w + x + y + z)
