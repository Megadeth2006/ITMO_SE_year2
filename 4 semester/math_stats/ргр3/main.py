import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# загрузка данных
df = pd.read_csv("RGR3_A_2.csv")

x = df["x"].to_numpy(dtype=float)
y = df["y"].to_numpy(dtype=float)
n = len(x)

# значение для прогноза
x_star = 41.1415


# 1. первичный анализ


print("число наблюдений n =", n)
print("среднее x =", np.mean(x))
print("среднее y =", np.mean(y))
print("минимальный x =", np.min(x))
print("максимальный x =", np.max(x))
print("коэффициент корреляции =", np.corrcoef(x, y)[0, 1])

plt.figure(figsize=(8, 5))
plt.scatter(x, y)
plt.title("Диаграмма рассеяния: кэш-память и производительность")
plt.xlabel("x — кэш-память, КБ")
plt.ylabel("y — относительная производительность, усл. ед.")
plt.grid(True, alpha=0.3)
plt.savefig("scatter.png", dpi=300, bbox_inches="tight")
plt.show()

# 2. линейная модель y = a + bx


X_lin = np.column_stack((np.ones(n), x))
a_lin, b_lin = np.linalg.lstsq(X_lin, y, rcond=None)[0]

y_lin = a_lin + b_lin * x

print("\nЛинейная модель:")
print(f"y = {a_lin:.4f} + {b_lin:.4f}x")


# 3. квадратичная модель y = a + bx + cx^2


X_quad = np.column_stack((np.ones(n), x, x ** 2))
a_quad, b_quad, c_quad = np.linalg.lstsq(X_quad, y, rcond=None)[0]

y_quad = a_quad + b_quad * x + c_quad * x ** 2

print("\nКвадратичная модель:")
print(f"y = {a_quad:.4f} + {b_quad:.4f}x + {c_quad:.4f}x^2")


# 4. степенная модель y = a * x^b
# ln(y) = ln(a) + b ln(x)


ln_x = np.log(x)
ln_y = np.log(y)

X_pow = np.column_stack((np.ones(n), ln_x))
ln_a_pow, b_pow = np.linalg.lstsq(X_pow, ln_y, rcond=None)[0]

a_pow = np.exp(ln_a_pow)
y_pow = a_pow * x ** b_pow

print("\nСтепенная модель:")
print(f"y = {a_pow:.4f} * x^{b_pow:.4f}")


# 5. сравнение моделей


def metrics(y_true, y_pred):
    residuals = y_true - y_pred
    rss = np.sum(residuals ** 2)
    tss = np.sum((y_true - np.mean(y_true)) ** 2)
    r2 = 1 - rss / tss
    rmse = np.sqrt(np.mean(residuals ** 2))
    avg_error = np.mean(np.abs(residuals / y_true)) * 100
    return rss, r2, rmse, avg_error

rss_lin, r2_lin, rmse_lin, aerr_lin = metrics(y, y_lin)
rss_quad, r2_quad, rmse_quad, aerr_quad = metrics(y, y_quad)
rss_pow, r2_pow, rmse_pow, aerr_pow = metrics(y, y_pow)

comparison = pd.DataFrame({
    "Модель": ["Линейная", "Квадратичная", "Степенная"],
    "R2": [r2_lin, r2_quad, r2_pow],
    "RMSE": [rmse_lin, rmse_quad, rmse_pow],
    "A, %": [aerr_lin, aerr_quad, aerr_pow],
    "RSS": [rss_lin, rss_quad, rss_pow]
})

print("\nСравнение моделей:")
print(comparison)


# 6. график моделей


x_grid = np.linspace(np.min(x), np.max(x), 300)

y_lin_grid = a_lin + b_lin * x_grid
y_quad_grid = a_quad + b_quad * x_grid + c_quad * x_grid ** 2
y_pow_grid = a_pow * x_grid ** b_pow

plt.figure(figsize=(8, 5))
plt.scatter(x, y, label="исходные данные")
plt.plot(x_grid, y_lin_grid, label="линейная")
plt.plot(x_grid, y_quad_grid, label="квадратичная")
plt.plot(x_grid, y_pow_grid, label="степенная")
plt.title("Три регрессионные модели на фоне данных")
plt.xlabel("x — кэш-память, КБ")
plt.ylabel("y — относительная производительность, усл. ед.")
plt.grid(True, alpha=0.3)
plt.legend()
plt.savefig("models.png", dpi=300, bbox_inches="tight")
plt.show()


# 7. график остатков


e_lin = y - y_lin
e_quad = y - y_quad
e_pow = y - y_pow

plt.figure(figsize=(8, 5))
plt.axhline(0, linewidth=1)
plt.scatter(x, e_lin, label="линейная")
plt.scatter(x, e_quad, label="квадратичная", marker="x")
plt.scatter(x, e_pow, label="степенная", marker="^")
plt.title("Остатки моделей")
plt.xlabel("x — кэш-память, КБ")
plt.ylabel("остаток e = y - ŷ")
plt.grid(True, alpha=0.3)
plt.legend()
plt.savefig("residuals.png", dpi=300, bbox_inches="tight")
plt.show()


# 8. подробный анализ линейной модели


x_mean = np.mean(x)
y_mean = np.mean(y)

Sxx = np.sum((x - x_mean) ** 2)
Sxy = np.sum((x - x_mean) * (y - y_mean))

s2 = rss_lin / (n - 2)
s = np.sqrt(s2)

SE_b = s / np.sqrt(Sxx)
SE_a = s * np.sqrt(1 / n + x_mean ** 2 / Sxx)

alpha = 0.05
dfree = n - 2
t_crit = stats.t.ppf(1 - alpha / 2, dfree)

ci_a = (a_lin - t_crit * SE_a, a_lin + t_crit * SE_a)
ci_b = (b_lin - t_crit * SE_b, b_lin + t_crit * SE_b)

t_obs = b_lin / SE_b
p_value = 2 * (1 - stats.t.cdf(abs(t_obs), dfree))

print("\nПодробный анализ линейной модели:")
print(f"a = {a_lin:.4f}")
print(f"b = {b_lin:.4f}")
print(f"Sxx = {Sxx:.2f}")
print(f"Sxy = {Sxy:.2f}")
print(f"RSS = {rss_lin:.2f}")
print(f"s^2 = {s2:.2f}")
print(f"s = {s:.2f}")
print(f"SE(a) = {SE_a:.2f}")
print(f"SE(b) = {SE_b:.2f}")
print(f"95% ДИ для a: [{ci_a[0]:.2f}; {ci_a[1]:.2f}]")
print(f"95% ДИ для b: [{ci_b[0]:.2f}; {ci_b[1]:.2f}]")
print(f"t наблюдаемое = {t_obs:.4f}")
print(f"t критическое = {t_crit:.4f}")
print(f"p-value = {p_value:.8f}")

if abs(t_obs) > t_crit:
    print("Вывод: H0 отвергается, коэффициент b статистически значим.")
else:
    print("Вывод: H0 не отвергается, коэффициент b статистически незначим.")

# 9. прогноз при x*


pred_lin = a_lin + b_lin * x_star
pred_quad = a_quad + b_quad * x_star + c_quad * x_star ** 2
pred_pow = a_pow * x_star ** b_pow

print("\nПрогноз при x* =", x_star)
print(f"Линейная модель: {pred_lin:.2f}")
print(f"Квадратичная модель: {pred_quad:.2f}")
print(f"Степенная модель: {pred_pow:.2f}")


# 10. таблицы для отчёта


calc_table = df.copy()
calc_table["y_lin"] = y_lin
calc_table["e_lin"] = e_lin
calc_table["y_quad"] = y_quad
calc_table["e_quad"] = e_quad
calc_table["y_pow"] = y_pow
calc_table["e_pow"] = e_pow

print("\nПервые 12 строк с прогнозами:")
print(calc_table.head(12).round(2))

# сохранение таблиц в Excel для удобства
with pd.ExcelWriter("rgr3_calculations.xlsx") as writer:
    df.to_excel(writer, sheet_name="data", index=False)
    comparison.to_excel(writer, sheet_name="model_comparison", index=False)
    calc_table.to_excel(writer, sheet_name="predictions_residuals", index=False)

print("\nФайлы scatter.png, models.png, residuals.png и rgr3_calculations.xlsx сохранены.")