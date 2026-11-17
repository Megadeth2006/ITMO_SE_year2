from __future__ import annotations

import math
from decimal import Decimal

from program_part.approximation_methods import (
    fit_exponential,
    fit_logarithmic,
    fit_polynomial,
    fit_power,
)
from program_part.io_utils import render_approximation_report
from program_part.models import ApproximationResult, ApproximationSolveResult, DataPoint
from program_part.number_utils import decimal_to_float


MIN_POINTS = 8
MAX_POINTS = 12


METHODS = [
    ("linear", "Линейная функция", lambda xs, ys: fit_polynomial(xs, ys, 1)),
    ("quadratic", "Полиномиальная функция 2-й степени", lambda xs, ys: fit_polynomial(xs, ys, 2)),
    ("cubic", "Полиномиальная функция 3-й степени", lambda xs, ys: fit_polynomial(xs, ys, 3)),
    ("exponential", "Экспоненциальная функция", fit_exponential),
    ("logarithmic", "Логарифмическая функция", fit_logarithmic),
    ("power", "Степенная функция", fit_power),
]


def build_variant_3_points() -> list[DataPoint]:
    points: list[DataPoint] = []
    x = Decimal("-2")
    step = Decimal("0.2")
    for _ in range(11):
        y = Decimal(4) * x / (x ** 4 + Decimal(3))
        points.append(DataPoint(x=x, y=y))
        x += step
    return points


def points_to_text(points: list[DataPoint]) -> str:
    return "\n".join(f"{point.x}; {point.y}" for point in points)


def _validate_points(points: list[DataPoint]) -> None:
    if not (MIN_POINTS <= len(points) <= MAX_POINTS):
        raise ValueError(f"Таблица должна содержать от {MIN_POINTS} до {MAX_POINTS} точек. Сейчас: {len(points)}.")

    xs = [point.x for point in points]
    if len(set(xs)) < 2:
        raise ValueError("В таблице должно быть хотя бы два различных значения x.")


def _convert_points(points: list[DataPoint]) -> tuple[list[float], list[float]]:
    xs = [decimal_to_float(point.x, f"x{index + 1}") for index, point in enumerate(points)]
    ys = [decimal_to_float(point.y, f"y{index + 1}") for index, point in enumerate(points)]
    return xs, ys


def _quality_message(r_squared: float | None) -> str:
    if r_squared is None:
        return "Коэффициент детерминации не вычислен."
    if r_squared >= 0.95:
        return "Высокая точность аппроксимации."
    if r_squared >= 0.75:
        return "Удовлетворительная точность аппроксимации."
    if r_squared >= 0.5:
        return "Слабая аппроксимация: модель описывает данные частично."
    return "Недостаточная аппроксимация: модель плохо описывает данные."


def _pearson_correlation(xs: list[float], ys: list[float]) -> float | None:
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    denominator_x = sum((x - mean_x) ** 2 for x in xs)
    denominator_y = sum((y - mean_y) ** 2 for y in ys)
    denominator = math.sqrt(denominator_x * denominator_y)
    if denominator == 0:
        return None
    return numerator / denominator


def _build_result(code: str, name: str, fitted_function, xs: list[float], ys: list[float]) -> ApproximationResult:
    phi_values = [fitted_function.evaluator(x) for x in xs]
    epsilon_values = [phi - y for phi, y in zip(phi_values, ys)]
    deviation_measure = sum(error ** 2 for error in epsilon_values)
    standard_deviation = math.sqrt(deviation_measure / len(xs))

    mean_y = sum(ys) / len(ys)
    total_sum = sum((y - mean_y) ** 2 for y in ys)
    if total_sum == 0:
        determination = 1.0 if deviation_measure < 1e-12 else 0.0
    else:
        determination = 1.0 - deviation_measure / total_sum

    return ApproximationResult(
        code=code,
        name=name,
        expression=fitted_function.expression,
        coefficients=fitted_function.coefficients,
        evaluator=fitted_function.evaluator,
        phi_values=phi_values,
        epsilon_values=epsilon_values,
        deviation_measure=deviation_measure,
        standard_deviation=standard_deviation,
        determination=determination,
        quality_message=_quality_message(determination),
    )


def _build_not_applicable_result(code: str, name: str, error_message: str) -> ApproximationResult:
    return ApproximationResult(
        code=code,
        name=name,
        expression="—",
        coefficients={},
        evaluator=None,
        phi_values=[],
        epsilon_values=[],
        deviation_measure=float("inf"),
        standard_deviation=float("inf"),
        determination=None,
        quality_message="Функция не применима к заданной таблице.",
        is_applicable=False,
        error_message=error_message,
    )


def solve_approximations(points: list[DataPoint]) -> ApproximationSolveResult:
    _validate_points(points)
    xs, ys = _convert_points(points)

    results: list[ApproximationResult] = []
    for code, name, fitter in METHODS:
        try:
            fitted_function = fitter(xs, ys)
            results.append(_build_result(code, name, fitted_function, xs, ys))
        except Exception as error:
            results.append(_build_not_applicable_result(code, name, str(error)))

    applicable_results = [result for result in results if result.is_applicable]
    if not applicable_results:
        raise ValueError("Ни одна аппроксимирующая функция не может быть построена для заданной таблицы.")

    best_result = min(applicable_results, key=lambda result: result.standard_deviation)
    pearson = _pearson_correlation(xs, ys)

    solve_result = ApproximationSolveResult(
        points=points,
        results=results,
        best_result=best_result,
        pearson_correlation=pearson,
        report="",
    )
    solve_result.report = render_approximation_report(solve_result)
    return solve_result
