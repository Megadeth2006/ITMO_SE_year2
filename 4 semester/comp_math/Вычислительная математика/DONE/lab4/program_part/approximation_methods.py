from __future__ import annotations
from typing import Callable, Any
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class FittedFunction:
    expression: str
    coefficients: dict[str, float]
    evaluator: Callable[..., Any]


def solveGauss(A: list[list[float]], B: list[float]) -> list[float]:
    """Решение СЛАУ методом Гаусса"""
    n = len(B)
    # Создаем расширенную матрицу M размером n x (n + 1)
    M = [[0.0] * (n + 1) for _ in range(n)]
    for i in range(n):
        for j in range(n):
            M[i][j] = A[i][j]
        M[i][n] = B[i]

    # Прямой ход метода Гаусса
    for i in range(n):
        maxRow = i
        maxValue = abs(M[i][i])
        # Поиск максимального элемента в столбце (частичный выбор)
        for k in range(i + 1, n):
            if abs(M[k][i]) > maxValue:
                maxValue = abs(M[k][i])
                maxRow = k

        # Перестановка строк
        temp = M[i]
        M[i] = M[maxRow]
        M[maxRow] = temp

        if abs(M[i][i]) < 1e-15:
            continue

        # Исключение элементов под главной диагональю
        for k in range(i + 1, n):
            tmp = M[k][i] / M[i][i]
            for j in range(i, n + 1):
                M[k][j] -= tmp * M[i][j]

    # Обратный ход метода Гаусса
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        sum_val = 0.0
        for j in range(i + 1, n):
            sum_val += M[i][j] * x[j]
        x[i] = (M[i][n] - sum_val) / M[i][i]

    return x


def fit_polynomial(xs: list[float], ys: list[float], degree: int) -> FittedFunction:
    """Полиномиальная аппроксимация"""
    n = len(xs)

    if degree == 1:
        sx = 0.0
        sy = 0.0
        sx2 = 0.0
        sxy = 0.0
        for i in range(n):
            x = xs[i]
            y=ys[i]
            sx += x
            sy += y
            sx2 += x**2
            sxy += x * y

        A = [[sx2, sx], [sx, n]]
        B = [sxy, sy]
        coefficients = solveGauss(A, B)

        a = coefficients[0]
        b = coefficients[1]

        def evaluate(x: float) -> float:
            return a * x + b

        return FittedFunction(
            expression="a1*x + a0",
            coefficients={"a1": a, "a0": b},
            evaluator=evaluate
        )

    elif degree == 2:
        sx = [0.0] * 5
        sxy = [0.0] * 3
        for k in range(5):
            sx[k] = sum(x ** k for x in xs)
        for k in range(3):
            sxy[k] = sum(y * (x ** k) for x, y in zip(xs, ys))

        A = [
            [sx[4], sx[3], sx[2]],
            [sx[3], sx[2], sx[1]],
            [sx[2], sx[1], sx[0]]
        ]
        B = [sxy[2], sxy[1], sxy[0]]
        c = solveGauss(A, B)

        def evaluate(x: float) -> float:
            return c[0] * x * x + c[1] * x + c[2]

        return FittedFunction(
            expression="a2*x^2 + a1*x + a0",
            coefficients={"a2": c[0], "a1": c[1], "a0": c[2]},
            evaluator=evaluate
        )

    elif degree == 3:
        sx = [0.0] * 7
        sxy = [0.0] * 4
        for k in range(7):
            sx[k] = sum(x ** k for x in xs)
        for k in range(4):
            sxy[k] = sum(y * (x ** k) for x, y in zip(xs, ys))

        A = [
            [sx[6], sx[5], sx[4], sx[3]],
            [sx[5], sx[4], sx[3], sx[2]],
            [sx[4], sx[3], sx[2], sx[1]],
            [sx[3], sx[2], sx[1], sx[0]]
        ]
        B = [sxy[3], sxy[2], sxy[1], sxy[0]]
        c = solveGauss(A, B)

        def evaluate(x: float) -> float:
            return c[0] * x * x * x + c[1] * x * x + c[2] * x + c[3]

        return FittedFunction(
            expression="a3*x^3 + a2*x^2 + a1*x + a0",
            coefficients={"a3": c[0], "a2": c[1], "a1": c[2], "a0": c[3]},
            evaluator=evaluate
        )
    else:
        raise ValueError("Поддерживаются только полиномы 1, 2 и 3 степени.")
    
def fit_exponential(xs: list[float], ys: list[float]) -> FittedFunction:
    if any(y <= 0 for y in ys):
        raise ValueError("экспоненциальная аппроксимация y = a*e^(b*x) требует y > 0 для всех точек")

    linPoints_y = [math.log(y) for y in ys]
    linRes = fit_polynomial(xs, linPoints_y, 1)

    a = math.exp(linRes.coefficients["a0"])
    b = linRes.coefficients["a1"]

    def evaluate(x: float) -> float:
        return a * math.exp(b * x)

    return FittedFunction("a*e^(b*x)", {"a": a, "b": b}, evaluate)


def fit_logarithmic(xs: list[float], ys: list[float]) -> FittedFunction:
    if any(x <= 0 for x in xs):
        raise ValueError("логарифмическая аппроксимация y = a*ln(x) + b требует x > 0 для всех точек")

    linPoints_x = [math.log(x) for x in xs]
    linRes = fit_polynomial(linPoints_x, ys, 1)

    a = linRes.coefficients["a1"]
    b = linRes.coefficients["a0"]

    def evaluate(x: float) -> float:
        return a * math.log(x) + b

    return FittedFunction("a*ln(x) + b", {"a": a, "b": b}, evaluate)


def fit_power(xs: list[float], ys: list[float]) -> FittedFunction:
    if any(x <= 0 for x in xs) or any(y <= 0 for y in ys):
        raise ValueError("степенная аппроксимация y = a*x^b требует x > 0 и y > 0 для всех точек")

    linPoints_x = [math.log(x) for x in xs]
    linPoints_y = [math.log(y) for y in ys]
    linRes = fit_polynomial(linPoints_x, linPoints_y, 1)

    a = math.exp(linRes.coefficients["a0"])
    b = linRes.coefficients["a1"]

    def evaluate(x: float) -> float:
        return a * (x ** b)

    return FittedFunction("a*x^b", {"a": a, "b": b}, evaluate)