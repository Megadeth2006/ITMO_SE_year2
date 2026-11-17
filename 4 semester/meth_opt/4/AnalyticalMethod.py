def f(x1, x2):
    return 6 * x1**2 + 5 * x1 * x2 + 6 * x2**2 - 17 * x1 - 17 * x2 + 17


def main():
    H = [[12, 5], [5, 12]]

    a11 = 12
    a12 = 5
    a21 = 5
    a22 = 12
    b1 = 17
    b2 = 17

    det = a11 * a22 - a12 * a21
    x1_min = (b1 * a22 - a12 * b2) / det
    x2_min = (a11 * b2 - b1 * a21) / det
    f_min = f(x1_min, x2_min)

    print(f"H = {H}")
    print(f"x_min = [{x1_min:.8f}, {x2_min:.8f}]")
    print(f"f_min = {f_min:.8f}")


if __name__ == "__main__":
    main()
