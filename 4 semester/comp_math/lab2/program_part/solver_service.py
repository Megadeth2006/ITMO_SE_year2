from __future__ import annotations

from dataclasses import dataclass

from program_part.equation_methods import (
    choose_fixed_end,
    choose_lambda,
    chord_method_fixed_end,
    count_sign_change_subintervals,
    secant_method,
    simple_iteration_q,
    simple_iteration_scalar_method,
)
from program_part.io_utils import (
    parse_equation_params,
    parse_system_params,
    render_chord_report,
    render_iteration_report,
    render_newton_system_report,
    render_secant_report,
)
from program_part.models import EquationProblem, SystemProblem
from program_part.system_methods import newton_system_method


@dataclass
class EquationSolveResult:
    method_code: str
    method_name: str
    root: float
    report: str
    rows: list
    a: float
    b: float
    eps: float


@dataclass
class SystemSolveResult:
    method_name: str
    root: tuple[float, float]
    report: str
    rows: list
    x0: float
    y0: float
    eps: float


def _validate_equation_interval(problem: EquationProblem, a: float, b: float) -> None:
    if a >= b:
        
        raise ValueError("Левая граница интервала должна быть меньше правой.")
    roots_count = count_sign_change_subintervals(problem.f, a, b)
    if roots_count == 0:
        raise ValueError("На заданном интервале не обнаружено корней.")
    if roots_count > 1:
        raise ValueError("На заданном интервале обнаружено несколько корней. Уточните границы.")



def solve_equation(method_code: str, problem: EquationProblem, raw_params: dict) -> EquationSolveResult:
    params = parse_equation_params(raw_params)
    
    
    a = params["a"]
    b = params["b"]
    eps = params["eps"]
    if eps <= 0:
        raise ValueError("Точность eps должна быть положительной.")

    _validate_equation_interval(problem, a, b)


    if method_code == "2":
        fixed, x0 = choose_fixed_end(problem, a, b)
        root, rows = chord_method_fixed_end(problem.f, fixed=fixed, x0=x0, eps=eps)
        report = render_chord_report(problem, root, rows, {"a": a, "b": b, "fixed": fixed, "x0": x0, "eps": eps})
        return EquationSolveResult("2", "Метод хорд", root, report, rows, a, b, eps)

    if method_code == "4":
        
        root, rows = secant_method(problem.f, x0=a, x1=b, eps=eps)
        report = render_secant_report(problem, root, rows, {"a": a, "b": b, "x0": a, "x1": b, "eps": eps})
        return EquationSolveResult("4", "Метод секущих", root, report, rows, a, b, eps)

    if method_code == "5":
        lam = choose_lambda(problem, a, b)
        q = simple_iteration_q(problem, a, b, lam)
        if q >= 1:
            raise ValueError("Для выбранного интервала не выполняется условие сходимости q < 1.")
        x0 = a if abs(problem.f(a)) < abs(problem.f(b)) else b
        phi = lambda x: x - lam * problem.f(x)
        root, rows = simple_iteration_scalar_method(problem.f, phi, x0=x0, eps=eps)
        report = render_iteration_report(
            problem,
            root,
            rows,
            {"a": a, "b": b, "x0": x0, "lambda": lam, "q": q, "eps": eps},
        )
        return EquationSolveResult("5", "Метод простой итерации", root, report, rows, a, b, eps)

    raise ValueError("Неизвестный метод для решения уравнения.")





def solve_system(problem: SystemProblem, raw_params: dict) -> SystemSolveResult:
    params = parse_system_params(raw_params)
    x0 = params["x0"]
    y0 = params["y0"]
    eps = params["eps"]
    if eps <= 0:
        raise ValueError("Точность eps должна быть положительной.")

    root, rows = newton_system_method(problem, x0=x0, y0=y0, eps=eps)
    report = render_newton_system_report(problem, root, rows, {"x0": x0, "y0": y0, "eps": eps})
    return SystemSolveResult("Метод Ньютона для систем", root, report, rows, x0, y0, eps)
