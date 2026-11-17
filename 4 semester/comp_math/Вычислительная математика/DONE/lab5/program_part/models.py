from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Callable

ScalarFunction = Callable[[float], float]

@dataclass(frozen=True)
class DataPoint:
    x: Decimal
    y: Decimal

@dataclass
class InterpolationResult:
    code: str
    name: str
    evaluator: ScalarFunction | None
    calculated_value: float | None
    is_applicable: bool = True
    error_message: str = ""

@dataclass
class InterpolationSolveResult:
    points: list[DataPoint]
    target_x: float
    results: list[InterpolationResult]
    finite_differences: list[list[float]] | None
    divided_differences: list[list[float]] | None
    report: str