from __future__ import annotations

from program_part.models import EquationProblem


def f_eq1(x: float) -> float:
    return x**3 + 2.84 * x**2 - 5.606 * x - 14.766


def df_eq1(x: float) -> float:
    return 3.0 * x**2 + 5.68 * x - 5.606


def f_eq2(x: float) -> float:
    return -1.38 * x**3 - 5.42 * x**2 + 2.57 * x + 10.95


def df_eq2(x: float) -> float:
    return -4.14 * x**2 - 10.84 * x + 2.57


def f_eq3(x: float) -> float:
    return x**3 - 4.5 * x**2 - 9.21 * x - 0.383


def df_eq3(x: float) -> float:
    return 3.0 * x**2 - 9.0 * x - 9.21


EQUATIONS: dict[str, EquationProblem] = {
    "1": EquationProblem(
        name="Вариант 3",
        expression="x^3 + 2.84x^2 - 5.606x - 14.766",
        f=f_eq1,
        df=df_eq1,
    ),
    "2": EquationProblem(
        name="Вариант 2",
        expression="-1.38x^3 - 5.42x^2 + 2.57x + 10.95",
        f=f_eq2,
        df=df_eq2,
    ),
    "3": EquationProblem(
        name="Вариант 12",
        expression="x^3 - 4.5x^2 - 9.21x - 0.383",
        f=f_eq3,
        df=df_eq3,
    ),
}
