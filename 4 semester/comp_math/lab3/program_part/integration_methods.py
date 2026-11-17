from __future__ import annotations


def left_rectangles(function, a: float, b: float, subdivisions: int) -> float:
    step = (b - a) / subdivisions
    total = 0.0

    for index in range(subdivisions):
        x_value = a + index * step
        total += function(x_value)

    return step * total


def right_rectangles(function, a: float, b: float, subdivisions: int) -> float:
    step = (b - a) / subdivisions
    total = 0.0

    for index in range(1, subdivisions + 1):
        x_value = a + index * step
        total += function(x_value)

    return step * total


def middle_rectangles(function, a: float, b: float, subdivisions: int) -> float:
    step = (b - a) / subdivisions
    total = 0.0

    for index in range(subdivisions):
        midpoint = a + (index + 0.5) * step
        total += function(midpoint)

    return step * total


def trapezoid_method(function, a: float, b: float, subdivisions: int) -> float:
    step = (b - a) / subdivisions
    total = (function(a) + function(b)) / 2.0

    for index in range(1, subdivisions):
        x_value = a + index * step
        total += function(x_value)

    return step * total


def simpson_method(function, a: float, b: float, subdivisions: int) -> float:
    if subdivisions % 2 != 0:
        subdivisions += 1

    step = (b - a) / subdivisions
    odd_sum = 0.0
    even_sum = 0.0

    for index in range(1, subdivisions):
        x_value = a + index * step
        if index % 2 == 0:
            even_sum += function(x_value)
        else:
            odd_sum += function(x_value)

    return step / 3.0 * (function(a) + function(b) + 4.0 * odd_sum + 2.0 * even_sum)


def newton_cotes_for_six_parts(function, a: float, b: float) -> float:
    step = (b - a) / 6.0
    x0 = a
    x1 = a + step
    x2 = a + 2.0 * step
    x3 = a + 3.0 * step
    x4 = a + 4.0 * step
    x5 = a + 5.0 * step
    x6 = b

    return 3.0 * step / 10.0 * (
        function(x0)
        + 5.0 * function(x1)
        + function(x2)
        + 6.0 * function(x3)
        + function(x4)
        + 5.0 * function(x5)
        + function(x6)
    )
