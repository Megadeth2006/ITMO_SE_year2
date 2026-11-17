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


def chord_method(a: float, b: float, delta: float = DELTA, max_iter: int = 10000):
    history = []
    fa = df(a)
    fb = df(b)

    if fa * fb > 0:
        raise ValueError("На концах отрезка df(a) и df(b) должны быть разных знаков.")

    for k in range(1, max_iter + 1):
        x = a - fa * (a - b) / (fa - fb)
        fx = df(x)
        history.append(
            {
                "k": k,
                "a": a,
                "b": b,
                "x": x,
                "dfx": fx,
            }
        )

        if abs(fx) < delta:
            return x, k, history

        if fx > 0:
            b = x
            fb = fx
        else:
            a = x
            fa = fx

    raise RuntimeError("Метод хорд не сошелся за max_iter итераций.")


def theoretical_iters_chord(history, x_star, delta):
    errors = [abs(row["x"] - x_star) for row in history]

    q = None
    for i in range(len(errors) - 2, -1, -1):
        if errors[i] > 0 and errors[i + 1] > 0:
            q = errors[i + 1] / errors[i]
            break

    if q is None or q <= 0 or q >= 1:
        return None

    e0 = errors[0]
    if e0 <= delta:
        return 0

    n = math.ceil(math.log(delta / e0) / math.log(q))
    return max(n, 0)


def print_result(theoretical_iters, actual_iters, x_min, table_rows):
    print("МЕТОД ХОРД")
    print(
        "1. Теоретическое кол-во итераций:",
        theoretical_iters if theoretical_iters is not None else "не удалось оценить",
    )
    print("2. Реальное кол-во итераций:", actual_iters)
    print("3. x_min:", format_float(x_min))
    print("4. f'(x_min):", format_float(df(x_min)))
    print("5. f(x_min):", format_float(f(x_min)))
    print("Таблица итераций:")
    print(format_table(["k", "a", "b", "x_k", "f'(x_k)"], table_rows))


x_star = newton_high_precision()
x_min, n_real, history = chord_method(1.0, 1.5, DELTA)
n_theor = theoretical_iters_chord(history, x_star, DELTA)
table_rows = [
    [
        row["k"],
        format_float(row["a"]),
        format_float(row["b"]),
        format_float(row["x"]),
        format_float(row["dfx"]),
    ]
    for row in history
]

print_result(n_theor, n_real, x_min, table_rows)
