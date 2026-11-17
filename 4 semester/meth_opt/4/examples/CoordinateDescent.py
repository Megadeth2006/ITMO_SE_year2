import math


# Целевая функция
def f(x1, x2):
    return 5 * x1 ** 2 + 3 * x1 * x2 + 5 * x2 ** 2 - 14 * x1 + 14 * x2 + 28


eps = 10 ** -8
x1 = -3.0
x2 = 1.0
iter_count = 0

while True:
    x1_old = x1
    x2_old = x2
    iter_count += 1

    # Шаг спуска: минимизация по x1 (приравняли df/dx1 к нулю)
    x1 = (14 - 3 * x2) / 10.0

    # Шаг спуска: минимизация по x2 (приравняли df/dx2 к нулю)
    x2 = (-14 - 3 * x1) / 10.0

    print(f"{iter_count}) x1 = {x1:.10f}, x2 = {x2:.10f}, f = {f(x1, x2):.10f}")

    # Норма разности между текущим и предыдущим приближением
    if math.sqrt((x1 - x1_old) ** 2 + (x2 - x2_old) ** 2) < eps:
        break

print(f"x_min = [{x1:.10f}, {x2:.10f}]")
print(f"f_min = {f(x1, x2):.10f}")