from __future__ import annotations
from matplotlib.figure import Figure
from models import InterpolationSolveResult
from number_utils import decimal_to_float

def draw_interpolation_on_figure(figure: Figure, result: InterpolationSolveResult) -> None:
    figure.clf()
    axis = figure.add_subplot(111)

    xs = [decimal_to_float(p.x, "") for p in result.points]
    ys = [decimal_to_float(p.y, "") for p in result.points]
    
    left, right = min(xs), max(xs)
    margin = (right - left) * 0.1 if right > left else 1.0
    grid_x = [left - margin + i * (right - left + 2*margin) / 500 for i in range(501)]

    colors = {
        "lagrange": "blue",
        "newton_fin": "green",
        "gauss": "red",
        "stirling": "purple",
        "bessel": "orange"
    }

    for res in result.results:
        if res.is_applicable and res.evaluator and res.code in colors:
            grid_y = [res.evaluator(x) for x in grid_x]
            axis.plot(grid_x, grid_y, color=colors[res.code], linewidth=1.5, alpha=0.7, label=res.name)


    axis.scatter(xs, ys, color="black", s=40, zorder=5, label="Узлы интерполяции")
    

    best_val = next((r.calculated_value for r in result.results if r.is_applicable), None)
    if best_val is not None:
        axis.scatter([result.target_x], [best_val], color="gold", edgecolor="black", s=100, zorder=6, label=f"Искомая точка X={result.target_x}")

    axis.axhline(0.0, linewidth=0.9, color="black")
    axis.grid(True, linestyle="--", alpha=0.6)
    axis.set_title("Интерполяция функции")
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.legend(loc="best", fontsize=8)
    figure.tight_layout()

def draw_placeholder(figure: Figure) -> None:
    figure.clf()
    axis = figure.add_subplot(111)
    axis.set_xlim(0, 1)
    axis.set_ylim(0, 1)
    axis.grid(True, linestyle="--", alpha=0.55)
    axis.set_title("График интерполяции")
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    figure.tight_layout()