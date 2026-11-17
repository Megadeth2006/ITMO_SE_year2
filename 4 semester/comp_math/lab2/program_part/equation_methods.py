from __future__ import annotations

import math

from program_part.models import ChordRow, EquationProblem, IterationRow, ScalarFunc, SecantRow


def count_sign_change_subintervals(f: ScalarFunc, a: float, b: float, parts: int = 400) -> int:
    
    count = 0
    step = (b - a) / parts
    x = a
    left = f(x)
    for _ in range(parts):
        x += step
        right = f(x)
        if math.isnan(left) or math.isnan(right):
            left = right
            continue
        if left == 0.0 or right == 0.0 or left * right < 0.0:
            count += 1
        left = right
        
    return count


def approximate_second_derivative(df: ScalarFunc, x: float, h: float = 1e-5) -> float:
    
    return (df(x + h) - df(x - h)) / (2.0 * h)


def choose_fixed_end(problem: EquationProblem, a: float, b: float) -> tuple[float, float]:
    fa = problem.f(a)
    
    fb = problem.f(b)
    d2a = approximate_second_derivative(problem.df, a)
    d2b = approximate_second_derivative(problem.df, b)

    if fa * d2a > 0:
        return a, b
    
    if fb * d2b > 0:
        return b, a
    return a, b


def choose_lambda(problem: EquationProblem, a: float, b: float) -> float:
    parts = 200
    
    step = (b - a) / parts
    derivs = [problem.df(a + i * step) for i in range(parts + 1)]
    max_abs = max(abs(value) for value in derivs)
    
    if max_abs < 1e-12:
        raise ValueError("Невозможно подобрать lambda: производная слишком мала на интервале.")

    avg = sum(derivs) / len(derivs)
    sign = 1.0 if avg >= 0 else -1.0
    base = 1.0 / max_abs
    candidates = [0.3, 0.5, 0.7, 0.9]

    best_lambda: float | None = None
    
    best_q = float("inf")
    for factor in candidates:
        lam = sign * factor * base
        q = max(abs(1.0 - lam * value) for value in derivs)
        if q < best_q:
            best_q = q
            
            best_lambda = lam

    if best_lambda is None or best_q >= 1.0:
        raise ValueError("Не удалось подобрать lambda так, чтобы выполнялось условие q < 1.")
    
    return best_lambda


def simple_iteration_q(problem: EquationProblem, a: float, b: float, lam: float) -> float:
    parts = 200
    
    step = (b - a) / parts
    return max(abs(1.0 - lam * problem.df(a + i * step)) for i in range(parts + 1))


def chord_method_fixed_end(
    f: ScalarFunc,
    fixed: float,
    x0: float,
    eps: float,
    max_iter: int = 100,
) -> tuple[float, list[ChordRow]]:
    
    fixed_value = f(fixed)
    xk = x0
    rows: list[ChordRow] = []

    for k in range(1, max_iter + 1):
        fxk = f(xk)
        denom = fxk - fixed_value
        if abs(denom) < 1e-14:
            raise ZeroDivisionError("В методе хорд знаменатель обратился в нуль.")

        xk1 = xk - fxk * (xk - fixed) / denom
        fxk1 = f(xk1)
        rows.append(ChordRow(k, xk, xk1, fxk1, abs(xk1 - xk)))
        if abs(xk1 - xk) < eps and abs(fxk1) < eps:
            return xk1, rows
        xk = xk1

    return xk, rows


def secant_method(
    f: ScalarFunc,
    
    x0: float,
    x1: float,
    eps: float,
    max_iter: int = 100,
) -> tuple[float, list[SecantRow]]:
    prev, curr = x0, x1
    rows: list[SecantRow] = []

    for k in range(1, max_iter + 1):
        f_prev = f(prev)
        f_curr = f(curr)
        denom = f_curr - f_prev
        
        if abs(denom) < 1e-14:
            raise ZeroDivisionError("В методе секущих знаменатель обратился в нуль.")

        nxt = curr - f_curr * (curr - prev) / denom
        fnxt = f(nxt)
        rows.append(SecantRow(k, prev, curr, nxt, fnxt, abs(nxt - curr)))
        if abs(nxt - curr) < eps and abs(fnxt) < eps:
            return nxt, rows
        
        prev, curr = curr, nxt

    return curr, rows


def simple_iteration_scalar_method(
    
    f: ScalarFunc,
    phi: ScalarFunc,
    
    x0: float,
    eps: float,
    max_iter: int = 100,
    
) -> tuple[float, list[IterationRow]]:
    xk = x0
    rows: list[IterationRow] = []

    for k in range(1, max_iter + 1):
        xk1 = phi(xk)
        fxk1 = f(xk1)
        
        rows.append(IterationRow(k, xk, xk1, fxk1, abs(xk1 - xk)))
        if abs(xk1 - xk) < eps and abs(fxk1) < eps:
            return xk1, rows
        xk = xk1

    return xk, rows
