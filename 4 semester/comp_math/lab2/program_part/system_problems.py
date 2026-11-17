from __future__ import annotations

import math

from program_part.models import SystemProblem


def sys1_f1(x: float, y: float) -> float:
    return math.cos(x - 1.0) + y - 0.5


def sys1_f2(x: float, y: float) -> float:
    return x - math.cos(y) - 3.0


def sys1_jac(x: float, y: float) -> tuple[tuple[float, float], tuple[float, float]]:
    return ((-math.sin(x - 1.0), 1.0), (1.0, math.sin(y)))


def sys2_f1(x: float, y: float) -> float:
    return math.tan(x * y + 0.1) - x**2


def sys2_f2(x: float, y: float) -> float:
    return x**2 + 2.0 * y**2 - 1.0


def sys2_jac(x: float, y: float) -> tuple[tuple[float, float], tuple[float, float]]:
    sec2 = 1.0 / math.cos(x * y + 0.1) ** 2
    return ((y * sec2 - 2.0 * x, x * sec2), (2.0 * x, 4.0 * y))


SYSTEMS: dict[str, SystemProblem] = {
    "1": SystemProblem(
        name="",
        expression="cos(x - 1) + y = 0.5; x - cos(y) = 3",
        f1=sys1_f1,
        f2=sys1_f2,
        jacobian=sys1_jac,
    ),
    "2": SystemProblem(
        name="",
        expression="tan(xy + 0.1) = x^2; x^2 + 2y^2 = 1",
        f1=sys2_f1,
        f2=sys2_f2,
        jacobian=sys2_jac,
    ),
}
