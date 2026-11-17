import numpy as np
import matplotlib.pyplot as plt
from numba import njit

# ---------------------------------------------------------
# 🔧 Основные параметры
width, height = 3000, 2000
xmin, xmax = -2.5, 1.0
ymin, ymax = -1.5, 1.5
max_iter = 1800
escape_radius = 100.0

# Цветовая палитра и контраст
cmap = 'twilight_shifted'  # фиолетово-синие неоновые оттенки
gamma = 0.5                # чуть мягче яркость
brightness = 1.3           # усиление свечения
# ---------------------------------------------------------


@njit(fastmath=True)
def mandelbrot(width, height, xmin, xmax, ymin, ymax, max_iter, escape_radius):
    img = np.zeros((height, width))
    for y in range(height):
        cy = y * (ymax - ymin) / (height - 1) + ymin
        for x in range(width):
            cx = x * (xmax - xmin) / (width - 1) + xmin
            c = complex(cx, cy)
            z = 0.0j
            for i in range(max_iter):
                if (z.real * z.real + z.imag * z.imag) > escape_radius**2:
                    smooth = i - np.log2(np.log2(abs(z))) + 4
                    img[y, x] = smooth
                    break
                z = z*z + c
            else:
                img[y, x] = max_iter
    return img


print("🌌 Рендерим ночной фрактал Мандельброта...")
data = mandelbrot(width, height, xmin, xmax, ymin, ymax, max_iter, escape_radius)
print("✅ Готово!")

# Коррекция контраста и свечения
data = (data / data.max()) ** gamma * brightness
data = np.clip(data, 0, 1)

# ---------------------------------------------------------
# 🎨 Отрисовка
fig, ax = plt.subplots(figsize=(10, 7))
img = ax.imshow(data, extent=(xmin, xmax, ymin, ymax),
                cmap=cmap, origin='lower', interpolation='bilinear')

ax.set_xticks([])
ax.set_yticks([])
ax.set_facecolor("black")
ax.set_title("Фрактал Мандельброта — Ночной стиль", fontsize=18, color="white", pad=15)
fig.patch.set_facecolor("black")

plt.tight_layout()
plt.savefig("mandelbrot_night.png", dpi=500, bbox_inches='tight', facecolor="black", pad_inches=0)
plt.show()
