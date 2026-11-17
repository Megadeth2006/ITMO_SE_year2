import numpy as np
import matplotlib.pyplot as plt
from numba import njit
import random

# 🎨 Насыщенные палитры (яркие, разноцветные)
cmap_choices = [
    "turbo",          # суперяркая спектральная радуга
    "nipy_spectral",  # мощный спектр — идеален для фракталов
    "gist_ncar",      # неоновые хаотичные цвета
    "hsv",            # чистая круговая радуга
    "plasma",         # мягкие огненно-розовые переливы
    "viridis",        # спокойная зелёно-синяя
    "inferno",        # тёплый контраст
    "twilight_shifted",# космические оттенки
    "cubehelix",      # светящиеся спирали
    "rainbow"         # классическая радуга
]

# ⚙️ Настройки изображения
width, height = 3000, 3000
xmin, xmax = -2.5, 1.0
ymin, ymax = -1.5, 1.5
max_iter = 1200
escape_radius = 100.0


# ⚡ Быстрая функция для фрактала Мандельброта
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


def show_mandelbrot(index=0):
    """Отображает Мандельброт с новой цветовой палитрой"""
    cmap = random.choice(cmap_choices)
    print(f"\n🌀 Мандельброт {index+1} | Палитра: {cmap}")

    data = mandelbrot(width, height, xmin, xmax, ymin, ymax, max_iter, escape_radius)

    fig, ax = plt.subplots(figsize=(12, 7))
    img = ax.imshow(data, extent=(xmin, xmax, ymin, ymax),
                    cmap=cmap, origin='lower', interpolation='bilinear')

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Множество Мандельброта — Палитра: {cmap}", fontsize=18, pad=15)
    plt.tight_layout()

    # 👉 при закрытии окна — новая палитра
    def on_close(event):
        next_index = index + 1
        show_mandelbrot(next_index)

    fig.canvas.mpl_connect('close_event', on_close)
    plt.show()


# 🚀 Запуск первого фрактала
show_mandelbrot(0)
