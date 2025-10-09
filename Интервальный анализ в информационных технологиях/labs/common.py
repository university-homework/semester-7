class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __add__(self, other):
        if isinstance(other, Interval):
            return Interval(self.start + other.start, self.end + other.end)
        if isinstance(other, (int, float)):
            return Interval(self.start + other, self.end + other)
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, (Interval, int, float)):
            return self.__add__(other)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Interval):
            return Interval(self.start - other.end, self.end - other.start)
        if isinstance(other, (int, float)):
            return Interval(self.start - other, self.end - other)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (Interval, int, float)):
            return self.__sub__(other)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Interval):
            multiplies = (self.start * other.start, self.start * other.end, self.end * other.start, self.end * other.end)
            return Interval(min(multiplies), max(multiplies))
        if isinstance(other, (int, float)):
            return Interval(self.start * other, self.end * other)
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (Interval, int, float)):
            return self.__mul__(other)
        return NotImplemented

    def __imul__(self, other):
        if isinstance(other, Interval):
            multiplies = (self.start * other.start, self.start * other.end, self.end * other.start, self.end * other.end)
            self.start = min(multiplies)
            self.end = max(multiplies)
            return self
        if isinstance(other, (int, float)):
            self.start *= other
            self.end *= other
            return self
        return NotImplemented

    def __pow__(self, power, modulo=None):
        if isinstance(power, (int, float)):
            result = Interval(self.start, self.end)
            for _ in range(power - 1):
                result = result * self
            return result
        return NotImplemented

    def __lt__(self, other):
        return self.end < other.start

    def __repr__(self):
        return f'Interval({self.start}, {self.end})'

    def __str__(self):
        return f'[{self.start}, {self.end}]'
