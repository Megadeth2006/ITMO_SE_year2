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
class ApproximationResult:
    code: str
    name: str
    expression: str
    coefficients: dict[str, float]
    evaluator: ScalarFunction | None
    phi_values: list[float]
    epsilon_values: list[float]
    deviation_measure: float
    standard_deviation: float
    determination: float | None
    quality_message: str
    is_applicable: bool = True
    error_message: str = ""


@dataclass
class ApproximationSolveResult:
    points: list[DataPoint]
    results: list[ApproximationResult]
    best_result: ApproximationResult
    pearson_correlation: float | None
    report: str
