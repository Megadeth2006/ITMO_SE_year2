import math

DELTA = 1e-8


def f(x: float) -> float:
    return x * x - 2 * x + math.exp(-x)


def df(x: float) -> float:
    return 2 * x - 2 - math.exp(-x)


def d2f(x: float) -> float:
    return 2 + math.exp(-x)


def format_float(value: float) -> str:
    return f"{value:.10f}"


def format_table(headers, rows):
    string_rows = [[str(cell) for cell in row] for row in rows]
    widths = [len(header) for header in headers]

    for row in string_rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    header_line = " | ".join(
        headers[index].ljust(widths[index]) for index in range(len(headers))
    )
    separator = "-+-".join("-" * widths[index] for index in range(len(headers)))
    data_lines = [
        " | ".join(row[index].ljust(widths[index]) for index in range(len(headers)))
        for row in string_rows
    ]

    return "\n".join([header_line, separator, *data_lines])


def newton_high_precision(x0: float = 1.5, tol: float = 1e-16, max_iter: int = 1000) -> float:
    x = x0
    for _ in range(max_iter):
        x_next = x - df(x) / d2f(x)
        if abs(x_next - x) < tol:
            return x_next
        x = x_next
    return x


def newton_method(x0: float, delta: float = DELTA, max_iter: int = 10000):
    x = x0
    history = []

    for k in range(1, max_iter + 1):
        dfx = df(x)
        d2fx = d2f(x)
        x_next = x - dfx / d2fx
        dfx_next = df(x_next)
        history.append(
            {
                "k": k,
                "x_prev": x,
                "dfx_prev": dfx,
                "d2fx_prev": d2fx,
                "x": x_next,
                "dfx": dfx_next,
            }
        )

        if abs(dfx_next) < delta:
            return x_next, k, history

        x = x_next

    raise RuntimeError("Метод Ньютона не сошелся за max_iter итераций.")


def theoretical_iters_newton(history, x_star, delta):
    if not history:
        return None

    errors = [abs(history[0]["x_prev"] - x_star)]
    errors.extend(abs(row["x"] - x_star) for row in history)

    c_value = None
    for i in range(len(errors) - 2, -1, -1):
        if errors[i] > 0 and errors[i + 1] > 0:
            c_value = errors[i + 1] / (errors[i] ** 2)
            break

    if c_value is None or c_value <= 0:
        return None

    e = errors[0]
    if e <= delta:
        return 0

    n = 0
    while e > delta and n < 1000:
        e = c_value * e * e
        n += 1

    return n if n < 1000 else None


def print_result(theoretical_iters, actual_iters, x_min, table_rows):
    print("МЕТОД НЬЮТОНА")
    print(
        "1. Теоретическое кол-во итераций:",
        theoretical_iters if theoretical_iters is not None else "не удалось оценить",
    )
    print("2. Реальное кол-во итераций:", actual_iters)
    print("3. x_min:", format_float(x_min))
    print("4. f'(x_min):", format_float(df(x_min)))
    print("5. f(x_min):", format_float(f(x_min)))
    print("Таблица итераций:")
    print(format_table(["k", "x_(k-1)", "f'(x_(k-1))", "f''(x_(k-1))", "x_k"], table_rows))


x_star = newton_high_precision()
x_min, n_real, history = newton_method(1.5, DELTA)
n_theor = theoretical_iters_newton(history, x_star, DELTA)
table_rows = [
    [
        row["k"],
        format_float(row["x_prev"]),
        format_float(row["dfx_prev"]),
        format_float(row["d2fx_prev"]),
        format_float(row["x"]),
    ]
    for row in history
]

print_result(n_theor, n_real, x_min, table_rows)
