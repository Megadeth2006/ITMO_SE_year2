import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import PowerNorm
from matplotlib import cm, colors
from IPython.display import HTML

# --- ПАРАМЕТРЫ ---
width, height = 400, 400
xmin, xmax = -2.0, 2.0
ymin, ymax = -2.0, 2.0
max_iter = 1000
escape_radius = 10.0
p = complex(-0.4, 0.0)
num_frames = 100

# --- СЕТКА ---
x = np.linspace(xmin, xmax, width)
y = np.linspace(ymin, ymax, height)
X, Y = np.meshgrid(x, y)
Z0 = X + 1j * Y
escape_radius_squared = escape_radius ** 2

# --- ФУНКЦИЯ ВЫЧИСЛЕНИЯ ---
def compute_phoenix_frame(c):
    Z = Z0.copy()
    Z_prev = np.zeros_like(Z)
    iters = np.zeros(Z.shape, dtype=int)
    mask = np.ones(Z.shape, dtype=bool)

    for i in range(max_iter):
        if not mask.any():
            break

        Z_active = Z[mask]
        Z_prev_active = Z_prev[mask]
        Z_new = Z_active**2 + c + p * Z_prev_active

        Z_prev[mask] = Z_active
        Z[mask] = Z_new

        escaped = (Z_new * np.conj(Z_new)).real > escape_radius_squared
        if np.any(escaped):
            escaped_mask = np.zeros_like(mask)
            escaped_mask[mask] = escaped
            iters[escaped_mask] = i
            mask[escaped_mask] = False

    iters[mask] = max_iter
    return iters

# --- ПОДГОТОВКА ПАЛИТРЫ ---
cmap = cm.get_cmap('inferno')
new_colors = cmap(np.linspace(0, 0.8, 256))  # убираем пересвеченные жёлтые тона
cmap_trunc = colors.ListedColormap(new_colors)

# --- ВИЗУАЛИЗАЦИЯ ---
fig, ax = plt.subplots(figsize=(8, 8))
fig.patch.set_facecolor("black")
ax.set_facecolor("black")

img = ax.imshow(np.zeros((height, width)),
                extent=(xmin, xmax, ymin, ymax),
                cmap=cmap_trunc,
                origin='lower',
                norm=PowerNorm(0.4, vmin=1, vmax=max_iter))

cbar = plt.colorbar(img)
cbar.set_label('Количество итераций', color='white')
cbar.ax.yaxis.set_tick_params(color='white')
plt.setp(cbar.ax.get_yticklabels(), color='white')

ax.set_xlabel('Re(z)', color='white')
ax.set_ylabel('Im(z)', color='white')
ax.tick_params(colors='white')

# --- АНИМАЦИЯ ---
def animate(frame):
    t = frame / num_frames * 2 * np.pi
    radius = 0.5  
    c_real = -0.5 + radius * np.cos(t)
    c_imag = 0.3 + radius * np.sin(t)
    c = complex(c_real, c_imag)

    frame_data = compute_phoenix_frame(c)
    img.set_array(frame_data)

    ax.set_title(f'Фрактал Феникса\nzₙ₊₁ = zₙ² + c + pzₙ₋₁\n'
                 f'c = {c_real:.3f} + {c_imag:.3f}i, p = {p.real:.2f}',
                 color='white')
    print(f"\r→ Генерация кадра {frame+1}/{num_frames}", end="")
    return [img]

animation = FuncAnimation(fig, animate, frames=num_frames,
                          interval=250, blit=True, repeat=True,
                          cache_frame_data=False)

plt.tight_layout()

# --- СОХРАНЕНИЕ ---
animation.save('phoenix_animation_balanced.gif', writer='pillow', fps=30)
print("\n✅ Анимация успешно сохранена: phoenix_animation_balanced.gif")
