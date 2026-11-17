from __future__ import annotations
import math
from decimal import Decimal

from interpolation_methods import (
    build_lagrange, build_newton_divided, build_gauss,
    build_stirling, build_bessel, is_equidistant, compute_finite_differences, compute_divided_differences
)
from models import InterpolationResult, InterpolationSolveResult, DataPoint
from number_utils import decimal_to_float, format_number

METHODS = [
    ("lagrange", "Многочлен Лагранжа", build_lagrange),
    ("newton_div", "Многочлен Ньютона (разделенные разности)", build_newton_divided),
    ("gauss", "Многочлен Гаусса", build_gauss),
    ("stirling", "Схема Стирлинга", build_stirling),
    ("bessel", "Схема Бесселя", build_bessel),
]

def build_variant_3_points() -> list[DataPoint]:
    xs = ["1.10", "1.25", "1.40", "1.55", "1.70", "1.85", "2.00"]
    ys = ["0.2234", "1.2438", "2.2644", "3.2984", "4.3222", "5.3516", "6.3867"]
    return [DataPoint(Decimal(x), Decimal(y)) for x, y in zip(xs, ys)]

def generate_from_function(func_name: str, a: float, b: float, n: int) -> list[DataPoint]:
    funcs = {
        "sin(x)": math.sin,
        "cos(x)": math.cos,
        "x^2 - 3x": lambda x: x**2 - 3*x
    }
    f = funcs[func_name]
    step = (b - a) / (n - 1)
    xs = [a + i * step for i in range(n)]
    return [DataPoint(Decimal(str(round(x, 5))), Decimal(str(round(f(x), 5)))) for x in xs]

def _convert_points(points: list[DataPoint]) -> tuple[list[float], list[float]]:
    xs = [decimal_to_float(p.x, f"x{i+1}") for i, p in enumerate(points)]
    ys = [decimal_to_float(p.y, f"y{i+1}") for i, p in enumerate(points)]
    return xs, ys

def render_interpolation_report(result: InterpolationSolveResult) -> str:
    lines = ["РЕЗУЛЬТАТЫ ИНТЕРПОЛЯЦИИ", ""]
    lines.append(f"Искомая точка X = {format_number(result.target_x)}")
    lines.append("")
    
    if result.finite_differences:
        lines.append("Тип сетки: Равноотстоящие узлы (используются конечные разности).")
    else:
        lines.append("Тип сетки: Неравномерная (используются разделенные разности).")
    
    lines.append("")

    lines.append("Значения функции в точке X:")
    lines.append("-" * 70)
    for res in result.results:
        if res.is_applicable:
            lines.append(f"{res.name:<42} | {format_number(res.calculated_value, 6)}")
        else:
            lines.append(f"{res.name:<42} | Не применимо ({res.error_message})")
    return "\n".join(lines)

def solve_interpolation(points: list[DataPoint], target_x_dec: Decimal) -> InterpolationSolveResult:
    if len(points) < 2:
        raise ValueError("Для интерполяции нужно минимум 2 точки.")
    
    xs, ys = _convert_points(points)
    target_x = decimal_to_float(target_x_dec, "Искомый X")

    fin_diffs = compute_finite_differences(ys) if is_equidistant(xs) else None
    div_diffs = compute_divided_differences(xs, ys)

    results = []
    for code, name, builder in METHODS:
        try:
            evaluator = builder(xs, ys)
            val = evaluator(target_x)
            results.append(InterpolationResult(code, name, evaluator, val))
        except Exception as e:
            results.append(InterpolationResult(code, name, None, None, False, str(e)))

    res = InterpolationSolveResult(points, target_x, results, fin_diffs, div_diffs, "")
    res.report = render_interpolation_report(res)
    return res