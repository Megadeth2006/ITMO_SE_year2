from __future__ import annotations

import math

from matplotlib.figure import Figure

from program_part.models import ApproximationSolveResult, DataPoint
from program_part.number_utils import decimal_to_float, format_number


def _point_floats(points: list[DataPoint]) -> tuple[list[float], list[float]]:
    xs = [decimal_to_float(point.x, f"x{index + 1}") for index, point in enumerate(points)]
    ys = [decimal_to_float(point.y, f"y{index + 1}") for index, point in enumerate(points)]
    return xs, ys


def _build_x_grid(left: float, right: float, count: int = 700) -> list[float]:
    if left == right:
        return [left]
    step = (right - left) / (count - 1)
    return [left + index * step for index in range(count)]


def _safe_curve(evaluator, x_grid: list[float]) -> tuple[list[float], list[float]]:
    xs: list[float] = []
    ys: list[float] = []
    for x in x_grid:
        try:
            y = evaluator(x)
        except Exception:
            continue
        if math.isfinite(y):
            xs.append(x)
            ys.append(y)
    return xs, ys


def create_approximation_figure(result: ApproximationSolveResult) -> Figure:
    xs, ys = _point_floats(result.points)
    left = min(xs)
    right = max(xs)
    width = right - left
    margin = 0.08 * width if width > 0 else 1.0
    grid = _build_x_grid(left - margin, right + margin)

    figure = Figure(figsize=(7.0, 4.8), dpi=100)
    axis = figure.add_subplot(111)

    axis.scatter(xs, ys, s=45, label="Исходные точки")

    for approximation in result.results:
        if not approximation.is_applicable or approximation.evaluator is None:
            continue
        curve_x, curve_y = _safe_curve(approximation.evaluator, grid)
        if not curve_x:
            continue
        label = f"{approximation.name}, СКО={format_number(approximation.standard_deviation, 5)}"
        linewidth = 2.6 if approximation.code == result.best_result.code else 1.4
        axis.plot(curve_x, curve_y, linewidth=linewidth, label=label)

    axis.axhline(0.0, linewidth=0.9)
    axis.axvline(0.0, linewidth=0.9)
    axis.grid(True, linestyle="--", linewidth=0.6, alpha=0.55)
    axis.set_xlim(left - margin, right + margin)
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.set_title("Аппроксимация табличной функции")
    axis.legend(loc="best", fontsize=8)
    figure.tight_layout()
    return figure


def create_placeholder_figure() -> Figure:
    figure = Figure(figsize=(7.0, 4.8), dpi=100)
    axis = figure.add_subplot(111)
    axis.set_xlim(0, 1)
    axis.set_ylim(0, 1)
    axis.grid(True, linestyle="--", linewidth=0.6, alpha=0.55)
    axis.set_title("Графики аппроксимирующих функций")
    figure.tight_layout()
    return figure
