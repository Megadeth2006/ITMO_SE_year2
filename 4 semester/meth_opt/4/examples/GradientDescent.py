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

# Фиксированный шаг спуска (выбран с учетом сходимости)
alpha = 0.1
iter_count = 0

while True:
    x1_old = x1
    x2_old = x2
    iter_count += 1

    # Вычисление градиента в текущей точке
    df_dx1, df_dx2 = grad_f(x1_old, x2_old)

    # Шаг спуска (движение по направлению антиградиента)
    x1 = x1_old - alpha * df_dx1
    x2 = x2_old - alpha * df_dx2

    print(f"{iter_count}) x1 = {x1:.10f}, x2 = {x2:.10f}, f = {f(x1, x2):.10f}")

    # Критерий останова по расстоянию между точками
    if math.sqrt((x1 - x1_old) ** 2 + (x2 - x2_old) ** 2) < eps:
        break

print(f"x_min = [{x1:.10f}, {x2:.10f}]")
print(f"f_min = {f(x1, x2):.10f}")