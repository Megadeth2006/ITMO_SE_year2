from __future__ import annotations

import math

import numpy as np
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from program_part.models import EquationProblem, SystemProblem


def create_equation_figure(problem: EquationProblem, a: float, b: float, root: float | None = None) -> Figure:
    margin = max(1.0, 0.2 * abs(b - a))
    left = a - margin
    right = b + margin
    xs = np.linspace(left, right, 800)
    ys = np.array([problem.f(float(x)) for x in xs], dtype=float)

    figure = Figure(figsize=(7.0, 4.8), dpi=100)
    axis = figure.add_subplot(111)
    axis.plot(xs, ys, color="royalblue", linewidth=1.8, label=f"{problem.expression} = 0")
    axis.axhline(0.0, color="black", linewidth=0.9)
    axis.axvline(0.0, color="black", linewidth=0.9)
    axis.grid(True, linestyle="--", linewidth=0.6, alpha=0.55)
    axis.set_xlim(left, right)
    y_abs = float(np.nanmax(np.abs(ys))) if ys.size else 1.0
    axis.set_ylim(-1.1 * max(1.0, y_abs), 1.1 * max(1.0, y_abs))
    axis.set_title(problem.name)
    if root is not None and math.isfinite(root):
        axis.scatter([root], [0.0], color="crimson", s=36, zorder=3, label=f"Корень: x ≈ {root:.6g}")
    axis.legend(loc="best")
    figure.tight_layout()
    return figure


def _system_bounds(x0: float, y0: float, root: tuple[float, float] | None) -> tuple[float, float, float, float]:
    if root is None:
        return x0 - 2.5, x0 + 2.5, y0 - 2.5, y0 + 2.5

    xr, yr = root
    margin_x = max(1.5, 0.35 * abs(xr - x0) + 1.0)
    margin_y = max(1.5, 0.35 * abs(yr - y0) + 1.0)
    x_min = min(x0, xr) - margin_x
    x_max = max(x0, xr) + margin_x
    y_min = min(y0, yr) - margin_y
    y_max = max(y0, yr) + margin_y
    return x_min, x_max, y_min, y_max


def create_system_figure(
    problem: SystemProblem,
    x_center: float,
    y_center: float,
    root: tuple[float, float] | None = None,
) -> Figure:
    x_min, x_max, y_min, y_max = _system_bounds(x_center, y_center, root)
    x_grid = np.linspace(x_min, x_max, 500)
    y_grid = np.linspace(y_min, y_max, 500)
    x_mesh, y_mesh = np.meshgrid(x_grid, y_grid)
    f1_values = np.vectorize(problem.f1)(x_mesh, y_mesh)
    f2_values = np.vectorize(problem.f2)(x_mesh, y_mesh)

    figure = Figure(figsize=(7.0, 4.8), dpi=100)
    axis = figure.add_subplot(111)
    axis.contour(x_mesh, y_mesh, f1_values, levels=[0.0], colors="royalblue", linewidths=1.8)
    axis.contour(x_mesh, y_mesh, f2_values, levels=[0.0], colors="crimson", linewidths=1.8)
    axis.axhline(0.0, color="black", linewidth=0.9)
    axis.axvline(0.0, color="black", linewidth=0.9)
    axis.grid(True, linestyle="--", linewidth=0.6, alpha=0.55)
    axis.set_xlim(x_min, x_max)
    axis.set_ylim(y_min, y_max)
    axis.set_title(problem.name)

    if root is not None:
        axis.scatter([root[0]], [root[1]], color="black", s=32, zorder=3)
        legend = [
            Line2D([0], [0], color="royalblue", lw=1.8, label="F1(x, y) = 0"),
            Line2D([0], [0], color="crimson", lw=1.8, label="F2(x, y) = 0"),
            Line2D([0], [0], marker="o", color="black", lw=0, label=f"Решение: ({root[0]:.6g}, {root[1]:.6g})"),
        ]
    else:
        legend = [
            Line2D([0], [0], color="royalblue", lw=1.8, label="F1(x, y) = 0"),
            Line2D([0], [0], color="crimson", lw=1.8, label="F2(x, y) = 0"),
        ]

    axis.legend(handles=legend, loc="best")
    figure.tight_layout()
    return figure


def save_equation_plot(problem: EquationProblem, a: float, b: float, path: str, root: float | None = None) -> None:
    figure = create_equation_figure(problem, a, b, root=root)
    figure.savefig(path, dpi=180)


def save_system_plot(
    problem: SystemProblem,
    x0: float,
    y0: float,
    path: str,
    root: tuple[float, float] | None = None,
) -> None:
    figure = create_system_figure(problem, x0, y0, root=root)
    figure.savefig(path, dpi=180)
