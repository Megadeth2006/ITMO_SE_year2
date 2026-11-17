from math import *


def f(x1, x2):
    return 6 * x1**2 + 5 * x1 * x2 + 6 * x2**2 - 17 * x1 - 17 * x2 + 17


def main():
    eps = 10 ** -8
    x1 = -2.0
    x2 = 5.0
    iter_count = 0

    while True:
        x1_old = x1
        x2_old = x2
        iter_count += 1

        x1 = (17 - 5 * x2) / 12.0
        x2 = (17 - 5 * x1) / 12.0

        print(f"{iter_count}) x1 = {x1:.10f}, x2 = {x2:.10f}, f = {f(x1, x2):.10f}")

        if sqrt((x1 - x1_old) ** 2 + (x2 - x2_old) ** 2) < eps:
            break

    print(f"x_min = [{x1:.10f}, {x2:.10f}]")
    print(f"f_min = {f(x1, x2):.10f}")


if __name__ == "__main__":
    main()
