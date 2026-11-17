import numpy as np
import matplotlib.pyplot as plt
from numba import njit
import random

# 🔮 Параметры фракталов
c_values = [
    complex(-0.8, 0.156),      # классика
    complex(-0.70176, -0.3842),# ветвистый
    complex(-0.4, 0.6),        # цветок
    complex(0.285, 0.01),      # волна
    complex(-0.74543, 0.11301),# спираль
    complex(-0.162, 1.04),     # энергия
    complex(-0.45, 0.1428),    # фрактальный цветок
]

# 🎨 РАЗНОЦВЕТНЫЕ ПАЛИТРЫ (яркие, контрастные)
cmap_choices = [
    "turbo",           # радужная энергия
    "viridis",         # зелёно-синяя гармония
    "inferno",         # огонь и тьма
    "twilight_shifted",# фиолетово-голубой космос
    "plasma",          # золотисто-розовые волны
    "cividis",         # золотисто-синяя наука
    "rainbow",         # чистая спектральная радуга 🌈
    "gist_ncar",       # хаотичная палитра (очень цветная!)
    "hsv",             # гладкая радуга
    "nipy_spectral"    # мощный спектр, идеален для фракталов
]

# ⚙️ Настройки
width, height = 1920, 1080
xmin, xmax = -1.7, 1.7
ymin, ymax = -1.1, 1.1
max_iter = 1000
escape_radius = 20.0


@njit(fastmath=True)
def julia(c, width, height, xmin, xmax, ymin, ymax, max_iter, escape_radius):
    img = np.zeros((height, width))
    for y in range(height):
        zy = y * (ymax - ymin) / (height - 1) + ymin
        for x in range(width):
            zx = x * (xmax - xmin) / (width - 1) + xmin
            z = complex(zx, zy)
            for i in range(max_iter):
                if (z.real * z.real + z.imag * z.imag) > escape_radius**2:
                    smooth = i - np.log2(np.log2(abs(z))) + 4
                    img[y, x] = smooth
                    break
                z = z*z + c
            else:
                img[y, x] = max_iter
    return img


def show_julia(index=0):
    """Отображает фрактал Жюлиа по индексу"""
    c = c_values[index % len(c_values)]
    cmap = random.choice(cmap_choices)  # 🎲 случайная палитра для каждой итерации

    print(f"\n🌀 Фрактал {index+1}/{len(c_values)}")
    print(f"   c = {c.real:+.4f}{c.imag:+.4f}i")
    print(f"   🎨 Палитра: {cmap}")

    data = julia(c, width, height, xmin, xmax, ymin, ymax, max_iter, escape_radius)

    fig, ax = plt.subplots(figsize=(12, 7))
    img = ax.imshow(data, extent=(xmin, xmax, ymin, ymax),
                    cmap=cmap, origin='lower', interpolation='bilinear')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Фрактал Жюлиа  |  c = {c.real:+.4f}{c.imag:+.4f}i", fontsize=18, pad=15)
    plt.tight_layout()

    # 👉 при закрытии окна — следующий фрактал
    def on_close(event):
        next_index = (index + 1) % len(c_values)
        show_julia(next_index)

    fig.canvas.mpl_connect('close_event', on_close)
    plt.show()


# 🚀 Старт
show_julia(0)
