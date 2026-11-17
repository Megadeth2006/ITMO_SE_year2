import numpy as np
import pandas as pd

edges = np.array([36, 40, 44, 47, 51, 55, 59, 62, 66], dtype=float)


freq = np.array([11, 14, 22, 21, 18, 25, 6, 3], dtype=float)


bins = list(zip(edges[:-1], edges[1:]))
widths = edges[1:] - edges[:-1]
midpoints = (edges[:-1] + edges[1:]) / 2

n = freq.sum()


xbar = (freq * midpoints).sum() / n

S = (freq * (midpoints - xbar) ** 2).sum()


var_biased = S / n        # смещенная
var_unbiased = S / (n-1)  # несмещенная


std_biased = np.sqrt(var_biased)
std_unbiased = np.sqrt(var_unbiased)

interval = (xbar - std_unbiased, xbar + std_unbiased)


df = pd.DataFrame({
    "Интервал": [f"[{a:g}; {b:g})" if i < len(bins)-1 else f"[{a:g}; {b:g}]"
                 for i, (a, b) in enumerate(bins)],
    "h": widths,
    "f_i": freq,
    "m_i": midpoints,
    "f_i*m_i": freq * midpoints,
    "(m_i-x̄)^2": (midpoints - xbar) ** 2,
    "f_i*(m_i-x̄)^2": freq * (midpoints - xbar) ** 2
})

print("n =", n)
print("x̄ =", xbar)
print("S =", S)
print("Смещенная дисперсия s^2 =", var_biased, " ; s =", std_biased)
print("Несмещенная дисперсия σ^2 =", var_unbiased, " ; σ =", std_unbiased)
print("[x̄-σ ; x̄+σ] =", interval)

print("\nТаблица расчетов:")
print(df)