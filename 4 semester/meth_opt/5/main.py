import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize


# данные варианта 11


X = np.array([0.85, 1.83, 2.91, 3.93, 4.86])
Y = np.array([1.12, 2.20, 3.12, 3.92, 4.94])
Z = np.array([0.73, 3.65, 4.86, 2.00, 0.32])

n = len(Z)


# задание 3
# константная модель


C_mse = np.mean(Z)
C_mae = np.median(Z)

print("Задание 3")
print(f"Лучшая константа по MSE: C = {C_mse:.4f}")
print(f"Лучшая константа по MAE: C = {C_mae:.4f}")
print()



# rbf-модель


def rbf_network(params, x, y):
    c1x, c1y, c2x, c2y, s1, s2, w1, w2, w0 = params

    phi1 = np.exp(-((x - c1x) ** 2 + (y - c1y) ** 2) / (2 * s1 ** 2))
    phi2 = np.exp(-((x - c2x) ** 2 + (y - c2y) ** 2) / (2 * s2 ** 2))

    return w1 * phi1 + w2 * phi2 + w0



# задание 4
# ручной расчёт первой итерации


# стратегия 2: два центра по двум группам точек
c1x_start = np.mean(X[:2])
c1y_start = np.mean(Y[:2])

c2x_start = np.mean(X[2:])
c2y_start = np.mean(Y[2:])

c1_start = np.array([c1x_start, c1y_start])
c2_start = np.array([c2x_start, c2y_start])

sigma_start = np.linalg.norm(c2_start - c1_start) / 2

w1_start = 0.1
w2_start = -0.1
w0_start = 0.0

def rbf_manual_values():
    d1 = (X - c1x_start) ** 2 + (Y - c1y_start) ** 2
    d2 = (X - c2x_start) ** 2 + (Y - c2y_start) ** 2

    phi1 = np.exp(-d1 / (2 * sigma_start ** 2))
    phi2 = np.exp(-d2 / (2 * sigma_start ** 2))

    z_pred = w1_start * phi1 + w2_start * phi2 + w0_start
    errors = z_pred - Z

    grad_w1 = np.mean(errors * phi1)
    grad_w2 = np.mean(errors * phi2)
    grad_w0 = np.mean(errors)

    grad_c1x = np.mean(errors * w1_start * phi1 * (X - c1x_start) / sigma_start ** 2)
    grad_c1y = np.mean(errors * w1_start * phi1 * (Y - c1y_start) / sigma_start ** 2)
    grad_c2x = np.mean(errors * w2_start * phi2 * (X - c2x_start) / sigma_start ** 2)
    grad_c2y = np.mean(errors * w2_start * phi2 * (Y - c2y_start) / sigma_start ** 2)

    grad_s1 = np.mean(errors * w1_start * phi1 * d1 / sigma_start ** 3)
    grad_s2 = np.mean(errors * w2_start * phi2 * d2 / sigma_start ** 3)

    return phi1, phi2, z_pred, errors, {
        "dL/dw1": grad_w1,
        "dL/dc1x": grad_c1x,
        "dL/dc1y": grad_c1y,
        "dL/dsigma1": grad_s1,
        "dL/dw2": grad_w2,
        "dL/dc2x": grad_c2x,
        "dL/dc2y": grad_c2y,
        "dL/dsigma2": grad_s2,
        "dL/dw0": grad_w0
    }


phi1, phi2, z_pred_start, errors_start, gradients = rbf_manual_values()

print("Задание 4")
print(f"c1 = ({c1x_start:.4f}, {c1y_start:.4f})")
print(f"c2 = ({c2x_start:.4f}, {c2y_start:.4f})")
print(f"sigma1 = sigma2 = {sigma_start:.4f}")
print(f"w1 = {w1_start}, w2 = {w2_start}, w0 = {w0_start}")
print()

print("Таблица значений для первой итерации:")
print("i | phi1 | phi2 | z_pred | error")
for i in range(n):
    print(f"{i + 1} | {phi1[i]:.4f} | {phi2[i]:.4f} | {z_pred_start[i]:.4f} | {errors_start[i]:.4f}")

print("\nГрадиенты:")
for name, value in gradients.items():
    print(f"{name} = {value:.4f}")

print()



# задание 5
# оптимизация rbf-сети


rbf_loss_history = []

def rbf_objective(params):
    c1x, c1y, c2x, c2y, s1, s2, w1, w2, w0 = params

    if s1 <= 0.1 or s2 <= 0.1:
        return 1e10

    predictions = rbf_network(params, X, Y)
    loss = 0.5 * np.mean((predictions - Z) ** 2)
    return loss


def rbf_callback(params):
    rbf_loss_history.append(rbf_objective(params))


# начальные центры берём в точках с двумя наибольшими z
top_indices = np.argsort(Z)[-2:][::-1]

initial_guess = [
    X[top_indices[0]], Y[top_indices[0]],
    X[top_indices[1]], Y[top_indices[1]],
    1.0, 1.0,
    Z[top_indices[0]], Z[top_indices[1]],
    0.0
]

bounds = [
    (0, 6), (0, 6),
    (0, 6), (0, 6),
    (0.1, 5), (0.1, 5),
    (-20, 20), (-20, 20),
    (-10, 10)
]

result = minimize(
    rbf_objective,
    initial_guess,
    method="L-BFGS-B",
    bounds=bounds,
    callback=rbf_callback,
    options={"maxiter": 1000, "ftol": 1e-15, "gtol": 1e-10}
)

p_opt = result.x
c1x, c1y, c2x, c2y, s1, s2, w1, w2, w0 = p_opt

print("Задание 5")
print("Оптимальные параметры RBF-сети:")
print(f"c1 = ({c1x:.4f}, {c1y:.4f})")
print(f"c2 = ({c2x:.4f}, {c2y:.4f})")
print(f"sigma1 = {s1:.4f}")
print(f"sigma2 = {s2:.4f}")
print(f"w1 = {w1:.4f}")
print(f"w2 = {w2:.4f}")
print(f"w0 = {w0:.4f}")
print(f"Финальная функция потерь: {result.fun:.8e}")
print()

z_final_pred = rbf_network(p_opt, X, Y)
final_errors = z_final_pred - Z

print("Проверка модели:")
print("i | x | y | z_real | z_pred | error")
for i in range(n):
    print(
        f"{i + 1} | {X[i]:.2f} | {Y[i]:.2f} | "
        f"{Z[i]:.4f} | {z_final_pred[i]:.4f} | {final_errors[i]:.2e}"
    )

print(f"\nОбычный MSE: {np.mean(final_errors ** 2):.8e}")
print(f"Максимальная абсолютная невязка: {np.max(np.abs(final_errors)):.8e}")



# график кривой обучения


plt.figure(figsize=(7, 5))
plt.plot(range(1, len(rbf_loss_history) + 1), rbf_loss_history, marker="o")
plt.yscale("log")
plt.xlabel("Номер итерации")
plt.ylabel("Функция потерь")
plt.title("Кривая обучения RBF-сети")
plt.grid(True, which="both", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig("task5_rbf_learning_curve_v11.png", dpi=300)
plt.show()



# 3d-поверхность и линии уровня


x_grid = np.linspace(0, 6, 100)
y_grid = np.linspace(0, 6, 100)
X_grid, Y_grid = np.meshgrid(x_grid, y_grid)

Z_grid = rbf_network(p_opt, X_grid, Y_grid)

fig = plt.figure(figsize=(12, 6))

ax1 = fig.add_subplot(121, projection="3d")
ax1.plot_surface(X_grid, Y_grid, Z_grid, cmap="viridis", alpha=0.75)
ax1.scatter(X, Y, Z, c="red", s=60, label="Исходные точки")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.set_zlabel("Z")
ax1.set_title("3D-визуализация RBF-модели")
ax1.legend()

ax2 = fig.add_subplot(122)
contour = ax2.contourf(X_grid, Y_grid, Z_grid, levels=25, cmap="viridis")
ax2.scatter(X, Y, c=Z, s=90, edgecolors="black", cmap="viridis", label="Исходные точки")
ax2.contour(X_grid, Y_grid, Z_grid, levels=10, colors="white", alpha=0.4, linewidths=0.5)
ax2.set_xlabel("X")
ax2.set_ylabel("Y")
ax2.set_title("Линии уровня RBF-модели")
ax2.grid(True, alpha=0.3)
ax2.legend()
plt.colorbar(contour, ax=ax2, label="Z")

plt.tight_layout()
plt.savefig("task5_rbf_surface_v11.png", dpi=300)
plt.show()