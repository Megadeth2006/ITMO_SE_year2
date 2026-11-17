from __future__ import annotations

import math

from matplotlib.figure import Figure

from program_part.models import IntegrationProblem, IntegrationSegment


def _build_points(function, left: float, right: float, count: int = 800) -> tuple[list[float], list[float]]:
    if left == right:
        try:
            value = function(left)
        except Exception:
            return [], []
        if math.isfinite(value):
            return [left], [value]
        return [], []

    step = (right - left) / (count - 1)
    x_values: list[float] = []
    y_values: list[float] = []

    for index in range(count):
        x_value = left + index * step
        try:
            y_value = function(x_value)
        except Exception:
            continue
        if math.isfinite(y_value):
            x_values.append(x_value)
            y_values.append(y_value)

    return x_values, y_values


def create_integration_figure(
    problem: IntegrationProblem,
    a: float,
    b: float,
    segments: list[IntegrationSegment] | None = None,
    excluded_segments: list[IntegrationSegment] | None = None,
    approximation: float | None = None,
) -> Figure:
    interval_left = min(a, b)
    interval_right = max(a, b)
    margin = max(1.0, 0.2 * abs(interval_right - interval_left))
    left = interval_left - margin
    right = interval_right + margin

    x_values, y_values = _build_points(problem.function, left, right)

    if segments is None:
        segments = [IntegrationSegment(interval_left, interval_right)]
    if excluded_segments is None:
        excluded_segments = []

    figure = Figure(figsize=(7.0, 4.8), dpi=100)
    axis = figure.add_subplot(111)
    axis.plot(x_values, y_values, color="royalblue", linewidth=1.8, label=f"f(x) = {problem.expression}")

    shaded_label_used = False
    for segment in segments:
        segment_x, segment_y = _build_points(problem.function, segment.left, segment.right, count=300)
        if segment_x:
            axis.fill_between(
                segment_x,
                segment_y,
                0.0,
                color="skyblue",
                alpha=0.35,
                label="Область интегрирования" if not shaded_label_used else None,
            )
            shaded_label_used = True

    skipped_label_used = False
    for segment in excluded_segments:
        axis.axvspan(
            segment.left,
            segment.right,
            color="lightcoral",
            alpha=0.18,
            label="Исключенный симметричный участок" if not skipped_label_used else None,
        )
        skipped_label_used = True

    axis.axhline(0.0, color="black", linewidth=0.9)
    axis.axvline(0.0, color="black", linewidth=0.9)
    axis.axvline(interval_left, color="darkgreen", linewidth=1.0, linestyle="--")
    axis.axvline(interval_right, color="darkgreen", linewidth=1.0, linestyle="--")
    axis.grid(True, linestyle="--", linewidth=0.6, alpha=0.55)
    axis.set_xlim(left, right)

    if y_values:
        max_abs_y = max(abs(value) for value in y_values)
    else:
        max_abs_y = 1.0
    axis.set_ylim(-1.1 * max(1.0, max_abs_y), 1.1 * max(1.0, max_abs_y))

    title = problem.name
    if approximation is not None:
        title += f", I ≈ {approximation:.6f}"
    axis.set_title(title)
    axis.legend(loc="best")
    figure.tight_layout()
    return figure


def create_placeholder_figure() -> Figure:
    figure = Figure(figsize=(7.0, 4.8), dpi=100)
    axis = figure.add_subplot(111)
    axis.set_xlim(0, 1)
    axis.set_ylim(0, 1)
    axis.grid(True, linestyle="--", linewidth=0.6, alpha=0.55)
    axis.set_title("График функции")
    figure.tight_layout()
    return figure
