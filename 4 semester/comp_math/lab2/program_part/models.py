from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


ScalarFunc = Callable[[float], float]
SystemFunc = Callable[[float, float], float]


@dataclass
class EquationProblem:
    name: str
    expression: str
    f: ScalarFunc
    df: ScalarFunc


@dataclass
class SystemProblem:
    name: str
    expression: str
    f1: SystemFunc
    f2: SystemFunc
    jacobian: Callable[[float, float], object]


@dataclass
class ChordRow:
    k: int
    xk: float
    xk1: float
    fxk1: float
    delta: float


@dataclass
class SecantRow:
    k: int
    xk_1: float
    xk: float
    xk1: float
    fxk1: float
    delta: float


@dataclass
class IterationRow:
    k: int
    xk: float
    xk1: float
    fxk1: float
    delta: float


@dataclass
class NewtonSystemRow:
    k: int
    xk: float
    yk: float
    xk1: float
    yk1: float
    dx: float
    dy: float
    f1_next: float
    f2_next: float
