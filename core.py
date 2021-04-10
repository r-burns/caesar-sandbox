from scipy.interpolate import CubicSpline

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

class Orbit:
    def __init__(self, start, spacing, posvel):
        times = [start + (spacing * i) for i in range(len(posvel))]
        self.data = CubicSpline(times, posvel)

    # get the azimuth times associated with each sample
    def times(self):
        return self.data.x

    # get the state-vector at a given azimuth time
    def __call__(self, t):
        return self.data(t)
