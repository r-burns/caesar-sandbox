class Interval:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def half_open_contains(self, value):
        return value >= self.min and value < self.max

class LinearSpace:
    def __init__(self, spacing, *, start=0):
        self.start = start
        self.spacing = spacing

    def index_of(self, value):
        return (value - self.start) / self.spacing
