import numpy as np
import matplotlib.pyplot as plt
from numba import njit

# === ⚙️ БАЗОВЫЕ НАСТРОЙКИ ===
width, height = 3000, 3000
xmin, xmax = -1.4, 1.4
ymin, ymax = -1.0, 1.0
max_iter = 1500
escape_radius = 30.0
cmap = "magma"  # "inferno", "plasma", "turbo", "twilight_shifted"...

# === 🧮 РАСЧЁТ ===
@njit(fastmath=True)
def phoenix(width, height, xmin, xmax, ymin, ymax, max_iter, escape_radius,
            c_real, c_imag, p_real, p_imag):
    img = np.zeros((height, width))
    escape_r2 = escape_radius ** 2

    for y in range(height):
        zy = y * (ymax - ymin) / (height - 1) + ymin
        for x in range(width):
            zx = x * (xmax - xmin) / (width - 1) + xmin
            z = complex(zx, zy)
            z_prev = 0.0j

            for i in range(max_iter):
                zr, zi = z.real, z.imag
                z_new_r = zr*zr - zi*zi + c_real + p_real*z_prev.real - p_imag*z_prev.imag
                z_new_i = 2*zr*zi + c_imag + p_real*z_prev.imag + p_imag*z_prev.real
                z_prev = z
                z = complex(z_new_r, z_new_i)

                if (z.real*z.real + z.imag*z.imag) > escape_r2:
                    smooth = i - np.log2(np.log2(abs(z) + 1e-6))
                    img[y, x] = smooth
                    break
    return img


# === 🌌 НОРМАЛИЗАЦИЯ ===
def normalize_astronomical(data, softness=10.0, gamma=1.25):
    data = np.log1p(data)
    data -= np.min(data)
    data /= np.max(data)
    data = np.arcsinh(data * softness) / np.arcsinh(softness)
    data = np.power(data, gamma)
    low, high = np.quantile(data, [0.002, 0.998])
    data = np.clip((data - low) / (high - low), 0, 1)
    return data


# === 🎨 ОТРИСОВКА ===
def render_phoenix(c, p, filename="phoenix.png"):
    print(f"\n⚙️ Генерация фрактала Феникса")
    print(f"   c = {c.real:+.4f}{c.imag:+.4f}i")
    print(f"   p = {p.real:+.4f}{p.imag:+.4f}i")

    data = phoenix(width, height, xmin, xmax, ymin, ymax,
                   max_iter, escape_radius, c.real, c.imag, p.real, p.imag)
    data = normalize_astronomical(data, softness=10.0, gamma=10)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(data, extent=(xmin, xmax, ymin, ymax),
              cmap=cmap, origin='lower', interpolation='bilinear')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(
        f"Фрактал Феникса: $z_{{n+1}} = z_n^2 + c + p z_{{n-1}}$\n"
        f"c = {c.real:+.3f}{c.imag:+.3f}i,   p = {p.real:+.3f}{p.imag:+.3f}i",
        fontsize=14, pad=10
    )
    plt.tight_layout()
    plt.savefig(filename, dpi=500, bbox_inches='tight')
    plt.close()
    print(f"✅ Сохранено как {filename}")


# === 🚀 ПРИМЕР ===
if __name__ == "__main__":
    c = complex(-0.125, 0.700)
    p = complex(-0.4, 0.0)
    render_phoenix(c, p, filename="phoenix_final.png")
