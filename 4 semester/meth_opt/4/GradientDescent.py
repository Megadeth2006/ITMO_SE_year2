from math import *


def f(x1, x2):
    return 6 * x1**2 + 5 * x1 * x2 + 6 * x2**2 - 17 * x1 - 17 * x2 + 17


def grad_f(x1, x2):
    df_dx1 = 12 * x1 + 5 * x2 - 17
    df_dx2 = 5 * x1 + 12 * x2 - 17
    return df_dx1, df_dx2


def main():
    eps = 10 ** -8
    x1 = -2.0
    x2 = 5.0
    alpha = 0.1
    iter_count = 0

    while True:
        x1_old = x1
        x2_old = x2
        iter_count += 1

        df_dx1, df_dx2 = grad_f(x1_old, x2_old)

        x1 = x1_old - alpha * df_dx1
        x2 = x2_old - alpha * df_dx2

        print(f"{iter_count}) x1 = {x1:.10f}, x2 = {x2:.10f}, f = {f(x1, x2):.10f}")

        if sqrt((x1 - x1_old) ** 2 + (x2 - x2_old) ** 2) < eps:
            break

    print(f"x_min = [{x1:.10f}, {x2:.10f}]")
    print(f"f_min = {f(x1, x2):.10f}")


if __name__ == "__main__":
    main()
