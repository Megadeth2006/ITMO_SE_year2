import sympy as sp

# В аналитическом методе итераций нет, эпсилон используем для формата вывода
eps = 10**-8

x1, x2 = sp.symbols('x1 x2')
f = 5*x1**2 + 3*x1*x2 + 5*x2**2 - 14*x1 + 14*x2 + 28

# Первые производные (градиент)
df_dx1 = sp.diff(f, x1)
df_dx2 = sp.diff(f, x2)

# print(f"df_dx1 = {df_dx1}")
# print(f"df_dx2 = {df_dx2}")

# Вторые производные (матрица Гесса)
H11 = sp.diff(df_dx1, x1)
H12 = sp.diff(df_dx1, x2)
H21 = sp.diff(df_dx2, x1)
H22 = sp.diff(df_dx2, x2)

H = sp.Matrix([[H11, H12], [H21, H22]])

# Поиск стационарной точки
solution = sp.solve([df_dx1, df_dx2], (x1, x2))

x1_min = float(solution[x1])
x2_min = float(solution[x2])
f_min = float(f.subs({x1: x1_min, x2: x2_min}))

print(f"x_min = [{x1_min:.8f}, {x2_min:.8f}]")
print(f"f_min = {f_min:.8f}")