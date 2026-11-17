import math


# Целевая функция
def f(x1, x2):
    return 5 * x1 ** 2 + 3 * x1 * x2 + 5 * x2 ** 2 - 14 * x1 + 14 * x2 + 28


# Компоненты вектора градиента
def grad_f(x1, x2):
    df_dx1 = 10 * x1 + 3 * x2 - 14
    df_dx2 = 3 * x1 + 10 * x2 + 14
    return df_dx1, df_dx2


eps = 10 ** -8
x1 = -3.0
x2 = 1.0
iter_count = 0

while True:
    x1_old = x1
    x2_old = x2
    iter_count += 1

    # Вычисление градиента в текущей точке
    g1, g2 = grad_f(x1_old, x2_old)

    # В методе наискорейшего спуска шаг alpha вычисляется аналитически для минимизации f вдоль направления антиградиента
    # Для квадратичной функции используется формула alpha = (g^T * g) / (g^T * H * g)
    # где H - матрица Гесса: [[10, 3], [3, 10]]
    alpha = (g1 ** 2 + g2 ** 2) / (10 * g1 ** 2 + 6 * g1 * g2 + 10 * g2 ** 2)

    # Шаг спуска
    x1 = x1_old - alpha * g1
    x2 = x2_old - alpha * g2

    print(f"{iter_count}) x1 = {x1:.10f}, x2 = {x2:.10f}, f = {f(x1, x2):.10f}")

    # Критерий останова по расстоянию между точками
    if math.sqrt((x1 - x1_old) ** 2 + (x2 - x2_old) ** 2) < eps:
        break

print(f"x_min = [{x1:.10f}, {x2:.10f}]")
print(f"f_min = {f(x1, x2):.10f}")