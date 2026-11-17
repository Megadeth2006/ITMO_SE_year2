import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Image parameters
width, height = 500, 500
xmin, xmax = -2.0, 2.0  # Real axis range
ymin, ymax = -2.0, 2.0  # Imaginary axis range

# Fractal parameters
c = complex(-0.2, 0.3)      # Complex parameter (fixed)
max_iter = 200             # Maximum iterations per point
escape_radius = 2.0        # Escape threshold

# Animation parameters
num_frames = 100           # Number of animation frames

# Create complex number grid
x = np.linspace(xmin, xmax, width)
y = np.linspace(ymin, ymax, height)
X, Y = np.meshgrid(x, y)

def compute_phoenix_frame(p):
    Z = X + 1j * Y
    Z_prev = np.zeros_like(Z)
    iters = np.zeros(Z.shape, dtype=int)
    
    # Phoenix formula iterations
    mask = np.ones(Z.shape, dtype=bool)
    for n in range(max_iter):
        Z_new = Z[mask]**2 + c + p * Z_prev[mask]
        Z_prev[mask] = Z[mask]
        Z[mask] = Z_new
        escaped = np.abs(Z) > escape_radius
        iters[escaped & mask] = n
        mask[escaped] = False
        if not mask.any():
            break
    
    return iters

# Create figure
fig, ax = plt.subplots(figsize=(8, 8))
img = ax.imshow(np.zeros((height, width)), extent=(xmin, xmax, ymin, ymax),
                cmap='inferno', origin='lower', vmin=0, vmax=max_iter)
plt.colorbar(img, label='Iterations')
ax.set_xlabel('Re(z)')
ax.set_ylabel('Im(z)')

# Animation function
def animate(frame):
    t = frame / num_frames * 2 * np.pi
    
    # p changes in a circle: p = center + radius * e^(it)
    p_center = complex(-0.5, 0.0)  # Center of p trajectory
    p_radius = 0.3                 # Radius of p trajectory
    p = p_center + p_radius * np.exp(1j * t)
    
    frame_data = compute_phoenix_frame(p)
    img.set_array(frame_data)
    ax.set_title(f'Phoenix Fractal: zₙ₊₁ = zₙ² + c + p·zₙ₋₁\n'
                 f'c = {c.real:.3f} + {c.imag:.3f}i, p = {p.real:.3f} + {p.imag:.3f}i')
    return [img]

# Create animation
animation = FuncAnimation(fig, animate, frames=num_frames,
                          interval=100, blit=True, repeat=True)

plt.tight_layout()
animation.save('phoenix_animation.gif', writer='pillow', fps=30)
plt.show()