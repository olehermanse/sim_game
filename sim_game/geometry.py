import math

def limit(number, lower, upper):
    assert lower < upper or (lower is None or upper is None)
    if lower and number < lower:
        number = lower
    if upper and number > upper:
        number = upper
    # TODO: remove these asserts and make tests
    assert number <= upper or not upper
    assert number >= lower or not lower
    return number

class Point:
    def __init__(self, x,y):
        self.x = x
        self.y = y

    def position(self):
        return (self.x, self.y)

    def xy(self):
        return (self.x, self.y)

    def set(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)

    def distance(self, other):
        x,y = self.x - other.x, self.y-other.y
        return math.sqrt(x**2 + y**2)

class Rectangle:
    def __init__(self, pos, dimensions, offset=Point(0.0,0.0)):
        self.position   = pos
        self.dimensions = dimensions
        self.offset     = offset

    def xy(self):
        return self.position.xy()

    def offset_xy(self):
        x,y = self.xy()
        w,h = self.dimensions.xy()
        ox, oy = self.offset.xy()
        x += w*ox/2
        y += h*oy/2
        return x,y

    def points(self):
        x,y = self.offset_xy()
        w,h = self.dimensions.xy()
        return (Point(x,     y),
                Point(x + w, y),
                Point(x + w, y + h),
                Point(x,     y + h))

    def contains_point(self, point):
        sx,sy = self.offset_xy()
        sw,sh = self.dimensions.xy()

        x,y = point.position()
        if (   x < sx
            or y < sy
            or x > sx + sw
            or y > sy + sh ):
            return False
        return True

    def contains_rectangle(self, rectangle):
        for p in rectangle.points():
            if p not in self:
                return False
        return True

    def collision(self, other):
        if type(other) is Point:
            return other in self
        for p in other.points():
            if p not in self:
                return False
        return True

    def __contains___(self, value):
        if type(value) is Point:
            return self.contains_point(value)
        if type(value) is Rectangle:
            return self.contains_rectangle(value)
        raise TypeError("Unknown type for contains")
