from __future__ import annotations

from program_part.models import NewtonSystemRow, SystemProblem


def solve_linear_2x2(
    a11: float,
    a12: float,
    a21: float,
    a22: float,
    b1: float,
    b2: float,
) -> tuple[float, float]:
    det = a11 * a22 - a12 * a21
    if abs(det) < 1e-14:
        raise ZeroDivisionError("Определитель матрицы Якоби слишком мал.")
    dx = (b1 * a22 - a12 * b2) / det
    dy = (a11 * b2 - b1 * a21) / det
    return dx, dy


def newton_system_method(
    problem: SystemProblem,
    x0: float,
    y0: float,
    eps: float,
    max_iter: int = 100,
) -> tuple[tuple[float, float], list[NewtonSystemRow]]:
    xk, yk = x0, y0
    rows: list[NewtonSystemRow] = []


    for k in range(1, max_iter + 1):
        jacobian = problem.jacobian(xk, yk)
        rhs1 = -problem.f1(xk, yk)
        rhs2 = -problem.f2(xk, yk)
        dx, dy = solve_linear_2x2(
            jacobian[0][0], # pyright: ignore[reportIndexIssue]
            jacobian[0][1], # pyright: ignore[reportIndexIssue]
            jacobian[1][0],  # pyright: ignore[reportIndexIssue]
            jacobian[1][1], # pyright: ignore[reportIndexIssue]
            rhs1,
            rhs2,
        )
        xk1, yk1 = xk + dx, yk + dy
        rows.append(
            NewtonSystemRow(
                k=k,
                xk=xk,
                yk=yk,
                xk1=xk1,
                yk1=yk1,
                dx=abs(dx),
                dy=abs(dy),
                f1_next=problem.f1(xk1, yk1),
                f2_next=problem.f2(xk1, yk1),
            )
        )
        if max(abs(dx), abs(dy), abs(rows[-1].f1_next), abs(rows[-1].f2_next)) < eps:
            return (xk1, yk1), rows
        xk, yk = xk1, yk1

    return (xk, yk), rows
