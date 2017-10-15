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

    def __getitem__(self, key):
        if type(key) is not int:
            raise TypeError
        return self.xy()[key]

    def distance(self, other):
        x,y = self.x - other.x, self.y-other.y
        return math.sqrt(x**2 + y**2)

class Rectangle:
    def __init__(self, pos, dimensions, anchor=(0,0), offset=(0,0)):
        self.position   = Point(*pos)
        self.dimensions = Point(*dimensions)
        self.offset     = Point(*offset)
        self.anchor     = Point(*anchor)

    def set_pos(self, x, y):
        self.position.set(x,y)

    def xy(self):
        return self.position.xy()

    def offset_xy(self):
        x,y = self.xy()
        ox, oy = self.offset.xy()
        x += ox
        y += oy
        return x,y

    def top_left(self):
        x,y = self.offset_xy()
        w,h = self.dimensions.xy()
        x,y = x-w/2, y-h/2
        ax, ay = self.anchor.xy()
        x = x + ax * w/2
        y = y + ay * h/2
        return x,y

    def points(self):
        x,y = self.top_left()
        w,h = self.dimensions.xy()
        return (Point(x,     y),
                Point(x + w, y),
                Point(x + w, y + h),
                Point(x,     y + h))

    def contains_point(self, point):
        point = Point(*point)
        sx,sy = self.top_left()
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
