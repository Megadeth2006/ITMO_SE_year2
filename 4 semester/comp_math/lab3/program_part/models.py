from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


ScalarFunc = Callable[[float], float]
IntervalValidator = Callable[[float, float], bool]
Integrator = Callable[[ScalarFunc, float, float, int], float]


@dataclass
class IntegrationProblem:
    code: str
    name: str
    expression: str
    function: ScalarFunc
    interval_validator: IntervalValidator


@dataclass
class IntegrationMethod:
    code: str
    name: str
    order: int
    integrator: Integrator


@dataclass
class IntegrationSegment:
    left: float
    right: float


@dataclass
class IterationRow:
    subdivisions: int
    current_value: float
    refined_value: float
    runge_error: float


@dataclass
class IntegrationSolveResult:
    method_code: str
    method_name: str
    problem_name: str
    problem_expression: str
    approximation: float
    runge_error: float
    subdivisions: int
    report: str
    rows: list[IterationRow]
    source_a: float
    source_b: float
    normalized_a: float
    normalized_b: float
    epsilon: float
    borders_were_swapped: bool
    active_segments: list[IntegrationSegment]
    excluded_segments: list[IntegrationSegment]
    singularity_notes: list[str]


@dataclass
class VariantReportRow:
    method_name: str
    approximation: float
    absolute_error: float
    relative_error_percent: float


@dataclass
class VariantReportResult:
    problem_name: str
    problem_expression: str
    a: float
    b: float
    exact_value: float
    rows: list[VariantReportRow]
    report: str
