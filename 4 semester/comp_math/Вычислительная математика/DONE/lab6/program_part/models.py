from dataclasses import dataclass
from typing import Callable

@dataclass
class OduEquation:
    display_name: str
    f: Callable[[float, float], float]
    exact: Callable[[float, float, float], float]

@dataclass
class MethodResult:
    name: str
    xs: list[float]
    ys: list[float]
    error: float
    error_criterion: str
    color: str

@dataclass
class SolveResult:
    equation: OduEquation
    exact_xs: list[float]
    exact_ys: list[float]
    methods_results: list[MethodResult]