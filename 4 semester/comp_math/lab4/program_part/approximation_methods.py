from __future__ import annotations
from typing import Callable, Any
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class FittedFunction:
    expression: str
    coefficients: dict[str, float]
    evaluator: Callable[..., Any]


EPSILON = 1e-12


def solve_linear_system(matrix: list[list[float]], vector: list[float]) -> list[float]:
    size = len(vector)
    a = [row[:] for row in matrix]
    b = vector[:]

    for column in range(size):
        pivot_row = max(range(column, size), key=lambda row: abs(a[row][column]))
        pivot = a[pivot_row][column]
        if abs(pivot) < EPSILON:
            raise ValueError("Система нормальных уравнений вырождена. Проверьте исходные точки.")

        if pivot_row != column:
            a[column], a[pivot_row] = a[pivot_row], a[column]
            b[column], b[pivot_row] = b[pivot_row], b[column]

        pivot = a[column][column]
        for j in range(column, size):
            a[column][j] /= pivot
        b[column] /= pivot

        for row in range(size):
            if row == column:
                continue
            factor = a[row][column]
            if abs(factor) < EPSILON:
                continue
            for j in range(column, size):
                a[row][j] -= factor * a[column][j]
            b[row] -= factor * b[column]

    return b


def least_squares_by_basis(xs: list[float], ys: list[float], basis_functions: list[Callable[..., Any]]) -> list[float]:
    size = len(basis_functions)
    matrix: list[list[float]] = []
    vector: list[float] = []

    basis_values = [[basis(x) for x in xs] for basis in basis_functions]

    for i in range(size):
        matrix_row: list[float] = []
        for j in range(size):
            matrix_row.append(sum(basis_values[i][k] * basis_values[j][k] for k in range(len(xs))))
        matrix.append(matrix_row)
        vector.append(sum(ys[k] * basis_values[i][k] for k in range(len(xs))))

    return solve_linear_system(matrix, vector)


def fit_polynomial(xs: list[float], ys: list[float], degree: int) -> FittedFunction:
    basis_functions = [lambda x, power=power: x ** power for power in range(degree + 1)]
    coefficients = least_squares_by_basis(xs, ys, basis_functions)

    def evaluate(x: float) -> float:
        return sum(coefficients[power] * x ** power for power in range(degree + 1))

    names = ["a0", "a1", "a2", "a3"]
    coefficient_map = {names[index]: coefficients[index] for index in range(degree + 1)}

    if degree == 1:
        expression = "a1*x + a0"
    elif degree == 2:
        expression = "a2*x^2 + a1*x + a0"
    elif degree == 3:
        expression = "a3*x^3 + a2*x^2 + a1*x + a0"
    else:
        expression = "polynomial"

    return FittedFunction(expression, coefficient_map, evaluate)


def fit_exponential(xs: list[float], ys: list[float]) -> FittedFunction:
    if any(y <= 0 for y in ys):
        raise ValueError("экспоненциальная аппроксимация y = a*e^(b*x) требует y > 0 для всех точек")

    transformed_y = [math.log(y) for y in ys]
    c0, c1 = least_squares_by_basis(xs, transformed_y, [lambda _x: 1.0, lambda x: x])
    a = math.exp(c0)
    b = c1

    def evaluate(x: float) -> float:
        return a * math.exp(b * x)

    return FittedFunction("a*e^(b*x)", {"a": a, "b": b}, evaluate)


def fit_logarithmic(xs: list[float], ys: list[float]) -> FittedFunction:
    if any(x <= 0 for x in xs):
        raise ValueError("логарифмическая аппроксимация y = a*ln(x) + b требует x > 0 для всех точек")

    c0, c1 = least_squares_by_basis(xs, ys, [lambda _x: 1.0, lambda x: math.log(x)])
    b = c0
    a = c1

    def evaluate(x: float) -> float:
        return a * math.log(x) + b

    return FittedFunction("a*ln(x) + b", {"a": a, "b": b}, evaluate)


def fit_power(xs: list[float], ys: list[float]) -> FittedFunction:
    if any(x <= 0 for x in xs):
        raise ValueError("степенная аппроксимация y = a*x^b требует x > 0 для всех точек")
    if any(y <= 0 for y in ys):
        raise ValueError("степенная аппроксимация y = a*x^b требует y > 0 для всех точек")

    transformed_x = [math.log(x) for x in xs]
    transformed_y = [math.log(y) for y in ys]
    c0, c1 = least_squares_by_basis(transformed_x, transformed_y, [lambda _x: 1.0, lambda x: x])
    a = math.exp(c0)
    b = c1

    def evaluate(x: float) -> float:
        return a * x ** b

    return FittedFunction("a*x^b", {"a": a, "b": b}, evaluate)
