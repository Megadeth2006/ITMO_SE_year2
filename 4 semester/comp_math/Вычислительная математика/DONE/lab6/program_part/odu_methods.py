def euler_method(f, x0, y0, xn, h, **kwargs):
    n = int(round((xn - x0) / h))
    xs = [x0 + i * h for i in range(n + 1)]
    ys = [y0]
    
    for i in range(n):
        y_next = ys[-1] + h * f(xs[i], ys[-1])
        ys.append(y_next)
        
    return xs, ys

def runge_kutta_4(f, x0, y0, xn, h, **kwargs):
    n = int(round((xn - x0) / h))
    xs = [x0 + i * h for i in range(n + 1)]
    ys = [y0]
    
    for i in range(n):
        x, y = xs[i], ys[-1]
        k1 = h * f(x, y)
        k2 = h * f(x + h/2, y + k1/2)
        k3 = h * f(x + h/2, y + k2/2)
        k4 = h * f(x + h, y + k3)
        
        y_next = y + (1/6) * (k1 + 2*k2 + 2*k3 + k4)
        ys.append(y_next)
        
    return xs, ys

def milne_method(f, x0, y0, xn, h, eps=1e-5):
    n = int(round((xn - x0) / h))
    if n < 4:
        return runge_kutta_4(f, x0, y0, xn, h)

   
    xs, ys = runge_kutta_4(f, x0, y0, x0 + 3*h, h)


    for i in range(4, n + 1):
        xs.append(x0 + i * h)

    for i in range(4, n + 1):
        f_im1 = f(xs[i-1], ys[i-1])
        f_im2 = f(xs[i-2], ys[i-2])
        f_im3 = f(xs[i-3], ys[i-3])
        
        
        y_prog = ys[i-4] + (4 * h / 3) * (2 * f_im3 - f_im2 + 2 * f_im1)
        
        
        y_corr = y_prog
        max_iters = 100
        for _ in range(max_iters):
            f_i_prog = f(xs[i], y_corr)
            
            y_corr_new = ys[i-2] + (h / 3) * (f_im2 + 4 * f_im1 + f_i_prog)
            
            
            if abs(y_corr_new - y_corr) < eps:
                y_corr = y_corr_new
                break
            y_corr = y_corr_new
            
        ys.append(y_corr)
        
    return xs, ys