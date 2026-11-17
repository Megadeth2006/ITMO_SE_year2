import math
from models import OduEquation, MethodResult, SolveResult
from odu_methods import euler_method, runge_kutta_4, milne_method

EQUATIONS = [
    OduEquation(
        display_name="y' = x + y",
        f=lambda x, y: x + y,
        exact=lambda x, x0, y0: (y0 + x0 + 1) * math.exp(x - x0) - x - 1
    ),
    OduEquation(
        display_name="y' = -y",
        f=lambda x, y: -y,
        exact=lambda x, x0, y0: y0 * math.exp(-(x - x0))
    ),
    OduEquation(
        display_name="y' = 2x",
        f=lambda x, y: 2 * x,
        exact=lambda x, x0, y0: x**2 + (y0 - x0**2)
    )
]

def solve_with_runge_adaptation(method, f, x0, y0, xn, initial_h, eps, p):
   
    cur_h = initial_h
    while True:
        xs_h, ys_h = method(f, x0, y0, xn, cur_h)
        xs_h2, ys_h2 = method(f, x0, y0, xn, cur_h / 2.0)
        
        
        err = abs(ys_h[-1] - ys_h2[-1]) / ((2**p) - 1)

        if err <= eps or cur_h < 1e-6:
            
            return xs_h, ys_h, err, cur_h
        
        cur_h /= 2.0

def calc_exact_error(xs, ys, exact_f, x0, y0):
    max_err = 0.0
    for x, y in zip(xs, ys):
        max_err = max(max_err, abs(exact_f(x, x0, y0) - y))
    return max_err

def solve_odu(eq_index: int, x0: float, y0: float, xn: float, h: float, eps: float) -> SolveResult:
    eq = EQUATIONS[eq_index]

    exact_xs = [x0 + i * (xn - x0) / 100.0 for i in range(101)]
    exact_ys = [eq.exact(x, x0, y0) for x in exact_xs]

    methods_results = []

    # 1. эйлер с адаптациепй шага по рунге
    xs_e, ys_e, err_e, h_e = solve_with_runge_adaptation(euler_method, eq.f, x0, y0, xn, h, eps, p=1)
    methods_results.append(MethodResult("Метод Эйлера", xs_e, ys_e, err_e, f"Правило Рунге (h={h_e:.5f})", "red"))

    # 2. рк4 с адаптацией шага по рунге
    xs_rk, ys_rk, err_rk, h_rk = solve_with_runge_adaptation(runge_kutta_4, eq.f, x0, y0, xn, h, eps, p=4)
    methods_results.append(MethodResult("Рунге-Кутта 4", xs_rk, ys_rk, err_rk, f"Правило Рунге (h={h_rk:.5f})", "blue"))

    # 3. милна, многошаговый
    xs_m, ys_m = milne_method(eq.f, x0, y0, xn, h, eps)
    err_m = calc_exact_error(xs_m, ys_m, eq.exact, x0, y0)
    methods_results.append(MethodResult("Метод Милна", xs_m, ys_m, err_m, "Точное решение", "green"))

    return SolveResult(eq, exact_xs, exact_ys, methods_results)