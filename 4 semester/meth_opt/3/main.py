from math import sin


EPSILON = 1e-8
A = 0.0
B = 1.0


def f(x: float) -> float:
    return x**3 - 3 * sin(x)


def parabolic_minimum(x1: float, x2: float, x3: float) -> float:
    f1, f2, f3 = f(x1), f(x2), f(x3)

    numerator = (x2 - x1) ** 2 * (f2 - f3) - (x2 - x3) ** 2 * (f2 - f1)
    denominator = 2 * ((x2 - x1) * (f2 - f3) - (x2 - x3) * (f2 - f1))

    if abs(denominator) < 1e-14:
        raise ZeroDivisionError(
            "Не удалось построить вершину параболы: знаменатель близок к нулю."
        )

    return x2 - numerator / denominator


def choose_initial_points(a: float, b: float, samples: int = 20) -> tuple[float, float, float]:
    xs = [a + i * (b - a) / samples for i in range(samples + 1)]
    ys = [f(x) for x in xs]

    min_index = min(range(len(xs)), key=lambda i: ys[i])
    if min_index == 0 or min_index == len(xs) - 1:
        raise ValueError(
            "Минимум на сетке оказался на границе отрезка, метод не запускается."
        )

    return xs[min_index - 1], xs[min_index], xs[min_index + 1]


def quadratic_approximation_method(
    a: float, b: float, epsilon: float, min_iterations: int = 3
) -> tuple[float, float, list[dict[str, float]]]:
    x1, x2, x3 = choose_initial_points(a, b)
    f1, f2, f3 = f(x1), f(x2), f(x3)

    if not (f2 <= f1 and f2 <= f3):
        raise ValueError("Начальные точки выбраны неудачно.")

    history: list[dict[str, float]] = []

    while True:
        u = parabolic_minimum(x1, x2, x3)
        u = min(max(u, x1), x3)
        fu = f(u)

        history.append(
            {
                "x1": x1,
                "x2": x2,
                "x3": x3,
                "u": u,
                "f(u)": fu,
            }
        )

        if len(history) >= min_iterations and abs(u - x2) < epsilon:
            return u, fu, history

        if u < x2:
            if fu <= f2:
                x3, f3 = x2, f2
                x2, f2 = u, fu
            else:
                x1, f1 = u, fu
        else:
            if fu <= f2:
                x1, f1 = x2, f2
                x2, f2 = u, fu
            else:
                x3, f3 = u, fu


def print_iterations(history: list[dict[str, float]]) -> None:
    print("Последовательность приближений:")
    for index, item in enumerate(history, start=1):
        print(
            f"{index}) "
            f"x1={item['x1']:.9f}, "
            f"x2={item['x2']:.9f}, "
            f"x3={item['x3']:.9f}, "
            f"u={item['u']:.9f}, "
            f"f(u)={item['f(u)']:.9f}"
        )


def print_iteration_summary(history: list[dict[str, float]]) -> None:
    print("Приближения по итерациям:")
    for index, item in enumerate(history, start=1):
        print(
            f"Итерация {index}: "
            f"x_min = {item['u']:.10f}, "
            f"f(x_min) = {item['f(u)']:.10f}"
        )


def main() -> None:
    xmin, fmin, history = quadratic_approximation_method(A, B, EPSILON)

    print("Метод квадратичной аппроксимации")
    print("Функция: f(x) = x^3 - 3*sin(x)")
    print(f"Отрезок: [{A}, {B}]")
    print(f"Погрешность: {EPSILON}")
    print()

    print_iterations(history)
    print()
    print(f"Точка минимума: x* = {xmin:.10f}")
    print(f"Значение функции: f(x*) = {fmin:.10f}")
    print(f"Количество итераций: {len(history)}")
    print()
    print_iteration_summary(history)


if __name__ == "__main__":
    main()
