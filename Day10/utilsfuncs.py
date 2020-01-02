"""
utilsfuncs.py
====================================
The core utility module for the Asteroid Finder.
"""


def load_input(filepath):
    """Function to return a list matrix of input map from file"""
    inputlist = []
    with open(filepath, "r") as inputfile:
        for line in inputfile:
            inputlist.append(line.rstrip())
    return inputlist


def lerp(start: int, end: int, t: float) -> float:
    """[L]inear int[erp]olation function. Returns a numebr between two other numbers.
    t=0.0 returns the start point, t=1.0 returns the end point"""

    return start + t * (end - start)


def lerp_point(p0: tuple, p1: tuple, t: float) -> tuple:
    """Linear interpolation function to be applied on points (tuples).
        Index [0] corresponds to the x axis, index [1] to the y axis"""

    return (lerp(p0[0], p1[0], t), lerp(p0[1], p1[1], t))


def round_point(p: tuple) -> tuple:
    """Rounds point coordinates (two-item tuple) to integer values."""

    return (round(p[0], None), round(p[1], None))


def diagonal_distance(p0: tuple, p1: tuple) -> int:
    """Returns the diagonal distance between two points (tuples) by returning greatest
    absolute difference between values of the same axis."""

    return max((abs(p0[0] - p1[0]), abs(p0[1] - p1[1])))


def line(p0: tuple, p1: tuple, includestartpoint: bool = False, roundline: bool = False) -> list:
    """Returns a list of line coordinates that is interpolated between two points (tuples).
    Uses linear interpolation algorithm.
    Optionally can include starting point in the results (default=False).
    Optionally can round line points to integer values (default=False)."""

    points = []
    N = diagonal_distance(p0, p1)
    for i in range(0, N):
        t = 0.0 if N == 0 else i / N
        if roundline:
            points.append(round_point(lerp_point(p0, p1, t)))
        else:
            points.append(lerp_point(p0, p1, t))

    return points if includestartpoint else points[1:]


def array_lookup(twodimarray: list, lookupvalue) -> list:
    """Lookups a specific value in a two dimensional array built from a list with nested lists.
    Returns coordinates of each found occurrence."""

    coordinates = []
    for y, yi in zip(twodimarray, range(0, len(twodimarray))):
        for x, xi in zip(y, range(0, len(y))):
            coordinates.append((xi, yi)) if x == lookupvalue else None

    return coordinates
