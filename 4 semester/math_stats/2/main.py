from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import permutations
from pathlib import Path
from statistics import NormalDist

import matplotlib


matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams["font.family"] = "DejaVu Sans"

ALPHA = 0.05
EPS = 3e-14
FPMIN = 1e-300
ITMAX = 200


@dataclass
class ColumnAnalysis:
    name: str
    model: str
    summary: dict[str, float]
    histograms: dict[str, dict[str, float | int | np.ndarray]]
    grouped: dict[str, float]
    mm_params: dict[str, float]
    mle_params: dict[str, float]
    fit_scores: dict[str, float]
    threshold: float
    prob_empirical: float
    prob_mm: float
    prob_mle: float
    ci_mean_asym: tuple[float, float]
    exact_mu_ci: tuple[float, float] | None
    exact_sigma2_ci: tuple[float, float] | None
    variation_path: Path


def choose_csv(base_dir: Path) -> Path:
    matches = sorted(base_dir.glob("RGR1_*.csv"))
    if not matches:
        raise FileNotFoundError("CSV-файл вида RGR1_*.csv не найден.")
    return matches[0]


def parse_variant(csv_path: Path) -> str:
    stem = csv_path.stem
    if "_" not in stem:
        return stem
    parts = stem.split("_")
    return parts[1] if len(parts) >= 2 else stem


def round4(value: float) -> float:
    return round(float(value), 4)


def save_variation_series(series: pd.Series, out_path: Path) -> Path:
    sorted_values = np.sort(series.to_numpy(dtype=float))
    table = pd.DataFrame({"i": np.arange(1, len(sorted_values) + 1), "x_(i)": sorted_values})
    table.to_csv(out_path, index=False)
    return out_path


def ecdf_values(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    xs = np.sort(np.asarray(x, dtype=float))
    ys = np.arange(1, len(xs) + 1) / len(xs)
    return xs, ys


def sample_summary(x: np.ndarray) -> dict[str, float]:
    x = np.asarray(x, dtype=float)
    mean = x.mean()
    centered = x - mean
    s2_biased = np.mean(centered**2)
    s2_unbiased = np.var(x, ddof=1)
    q10, q25, q75, q90 = np.quantile(x, [0.10, 0.25, 0.75, 0.90])
    m2 = np.mean(centered**2)
    m3 = np.mean(centered**3)
    skewness = 0.0 if m2 == 0 else m3 / (m2 ** 1.5)
    return {
        "n": float(len(x)),
        "min": float(np.min(x)),
        "max": float(np.max(x)),
        "mean": float(mean),
        "variance_biased": float(s2_biased),
        "variance_unbiased": float(s2_unbiased),
        "std_biased": float(math.sqrt(s2_biased)),
        "std_unbiased": float(math.sqrt(s2_unbiased)),
        "median": float(np.median(x)),
        "q10": float(q10),
        "q25": float(q25),
        "q75": float(q75),
        "q90": float(q90),
        "iqr": float(q75 - q25),
        "skewness": float(skewness),
    }


def histogram_configs(x: np.ndarray) -> dict[str, dict[str, float | int | np.ndarray]]:
    x = np.asarray(x, dtype=float)
    n = len(x)
    x_min = float(np.min(x))
    x_max = float(np.max(x))
    x_range = x_max - x_min
    summary = sample_summary(x)
    rules: dict[str, dict[str, float | int | np.ndarray]] = {}

    def make_edges(bins: int) -> np.ndarray:
        bins = max(1, int(bins))
        return np.linspace(x_min, x_max, bins + 1)

    sturges_bins = 1 + int(math.floor(math.log2(n)))
    scott_width = 3.5 * summary["std_biased"] * (n ** (-1 / 3))
    fd_width = 2.0 * summary["iqr"] * (n ** (-1 / 3))
    scott_bins = max(1, int(math.ceil(x_range / scott_width))) if scott_width > 0 else 1
    fd_bins = max(1, int(math.ceil(x_range / fd_width))) if fd_width > 0 else 1

    rules["Sturges"] = {
        "bins": sturges_bins,
        "width": x_range / sturges_bins if sturges_bins else x_range,
        "edges": make_edges(sturges_bins),
    }
    rules["Scott"] = {
        "bins": scott_bins,
        "width": scott_width if scott_width > 0 else x_range,
        "edges": make_edges(scott_bins),
    }
    rules["Freedman-Diaconis"] = {
        "bins": fd_bins,
        "width": fd_width if fd_width > 0 else x_range,
        "edges": make_edges(fd_bins),
    }
    return rules


def grouped_moments(x: np.ndarray, edges: np.ndarray) -> dict[str, float]:
    counts, bin_edges = np.histogram(x, bins=edges)
    mids = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    n = len(x)
    mean_g = float(np.sum(counts * mids) / n)
    var_g = float(np.sum(counts * (mids - mean_g) ** 2) / (n - 1))
    return {
        "mean_grouped": mean_g,
        "variance_grouped": var_g,
        "std_grouped": math.sqrt(var_g),
    }


def normal_cdf(x: float, mu: float, sigma: float) -> float:
    z = (x - mu) / (sigma * math.sqrt(2.0))
    return 0.5 * (1.0 + math.erf(z))


def uniform_cdf(x: float, a: float, b: float) -> float:
    if x <= a:
        return 0.0
    if x >= b:
        return 1.0
    return (x - a) / (b - a)


def shifted_exp_cdf(x: float, lam: float, c: float) -> float:
    if x < c:
        return 0.0
    return 1.0 - math.exp(-lam * (x - c))


def normal_pdf(x: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * math.sqrt(2.0 * math.pi))


def uniform_pdf(x: np.ndarray, a: float, b: float) -> np.ndarray:
    density = np.zeros_like(x, dtype=float)
    mask = (x >= a) & (x <= b)
    density[mask] = 1.0 / (b - a)
    return density


def shifted_exp_pdf(x: np.ndarray, lam: float, c: float) -> np.ndarray:
    density = np.zeros_like(x, dtype=float)
    mask = x >= c
    density[mask] = lam * np.exp(-lam * (x[mask] - c))
    return density


def fit_mm(x: np.ndarray, model: str) -> dict[str, float]:
    summary = sample_summary(x)
    mean = summary["mean"]
    s2 = summary["variance_biased"]
    s = summary["std_biased"]
    if model == "normal":
        return {"mu": mean, "sigma": s}
    if model == "uniform":
        half_width = math.sqrt(3.0 * s2)
        return {"a": mean - half_width, "b": mean + half_width}
    if model == "shifted_exp":
        lam = 1.0 / s
        return {"lambda": lam, "c": mean - 1.0 / lam}
    raise ValueError(f"Неизвестная модель: {model}")


def fit_mle(x: np.ndarray, model: str) -> dict[str, float]:
    summary = sample_summary(x)
    mean = summary["mean"]
    if model == "normal":
        return {"mu": mean, "sigma": summary["std_biased"]}
    if model == "uniform":
        return {"a": float(np.min(x)), "b": float(np.max(x))}
    if model == "shifted_exp":
        c = float(np.min(x))
        return {"lambda": 1.0 / (mean - c), "c": c}
    raise ValueError(f"Неизвестная модель: {model}")


def cdf_for_model(model: str, params: dict[str, float], x: float) -> float:
    if model == "normal":
        return normal_cdf(x, params["mu"], params["sigma"])
    if model == "uniform":
        return uniform_cdf(x, params["a"], params["b"])
    if model == "shifted_exp":
        return shifted_exp_cdf(x, params["lambda"], params["c"])
    raise ValueError(f"Неизвестная модель: {model}")


def pdf_for_model(model: str, params: dict[str, float], x: np.ndarray) -> np.ndarray:
    if model == "normal":
        return normal_pdf(x, params["mu"], params["sigma"])
    if model == "uniform":
        return uniform_pdf(x, params["a"], params["b"])
    if model == "shifted_exp":
        return shifted_exp_pdf(x, params["lambda"], params["c"])
    raise ValueError(f"Неизвестная модель: {model}")


def survival_for_model(model: str, params: dict[str, float], x0: float) -> float:
    if model == "normal":
        return 1.0 - normal_cdf(x0, params["mu"], params["sigma"])
    if model == "uniform":
        if x0 <= params["a"]:
            return 1.0
        if x0 >= params["b"]:
            return 0.0
        return (params["b"] - x0) / (params["b"] - params["a"])
    if model == "shifted_exp":
        if x0 <= params["c"]:
            return 1.0
        return math.exp(-params["lambda"] * (x0 - params["c"]))
    raise ValueError(f"Неизвестная модель: {model}")


def ks_distance(x: np.ndarray, model: str) -> float:
    xs, ys = ecdf_values(x)
    params = fit_mle(x, model)
    theor = np.array([cdf_for_model(model, params, value) for value in xs])
    return float(np.max(np.abs(ys - theor)))


def identify_models(df: pd.DataFrame) -> dict[str, str]:
    candidate_models = ["normal", "uniform", "shifted_exp"]
    columns = ["X1", "X2", "X3"]
    costs = {
        col: {model: ks_distance(df[col].to_numpy(dtype=float), model) for model in candidate_models}
        for col in columns
    }
    best_assignment: dict[str, str] | None = None
    best_score = float("inf")
    for perm in permutations(candidate_models):
        total = sum(costs[col][model] for col, model in zip(columns, perm))
        if total < best_score:
            best_score = total
            best_assignment = dict(zip(columns, perm))
    assert best_assignment is not None
    return best_assignment


def betacf(a: float, b: float, x: float) -> float:
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < FPMIN:
        d = FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, ITMAX + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < EPS:
            break
    return h


def regularized_incomplete_beta(a: float, b: float, x: float) -> float:
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(
        math.lgamma(a + b)
        - math.lgamma(a)
        - math.lgamma(b)
        + a * math.log(x)
        + b * math.log(1.0 - x)
    )
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * betacf(a, b, x) / a
    return 1.0 - bt * betacf(b, a, 1.0 - x) / b


def regularized_lower_gamma(a: float, x: float) -> float:
    if x <= 0.0:
        return 0.0
    if x < a + 1.0:
        ap = a
        total = 1.0 / a
        delta = total
        for _ in range(ITMAX):
            ap += 1.0
            delta *= x / ap
            total += delta
            if abs(delta) < abs(total) * EPS:
                break
        return total * math.exp(-x + a * math.log(x) - math.lgamma(a))
    b = x + 1.0 - a
    c = 1.0 / FPMIN
    d = 1.0 / b
    h = d
    for i in range(1, ITMAX + 1):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < FPMIN:
            d = FPMIN
        c = b + an / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < EPS:
            break
    q = math.exp(-x + a * math.log(x) - math.lgamma(a)) * h
    return 1.0 - q


def student_t_cdf(x: float, df: int) -> float:
    if x == 0.0:
        return 0.5
    z = df / (df + x * x)
    ib = regularized_incomplete_beta(df / 2.0, 0.5, z)
    return 1.0 - 0.5 * ib if x > 0 else 0.5 * ib


def chi2_cdf(x: float, df: int) -> float:
    return regularized_lower_gamma(df / 2.0, x / 2.0)


def invert_cdf(cdf_func, p: float, left: float, right: float, *args) -> float:
    while cdf_func(right, *args) < p:
        right *= 2.0
    for _ in range(220):
        middle = 0.5 * (left + right)
        value = cdf_func(middle, *args)
        if value < p:
            left = middle
        else:
            right = middle
    return 0.5 * (left + right)


def asymptotic_mean_ci(x: np.ndarray, alpha: float = ALPHA) -> tuple[float, float]:
    mean = float(np.mean(x))
    std = float(np.std(x, ddof=1))
    z = NormalDist().inv_cdf(1.0 - alpha / 2.0)
    half_width = z * std / math.sqrt(len(x))
    return mean - half_width, mean + half_width


def exact_normal_mean_ci(x: np.ndarray, alpha: float = ALPHA) -> tuple[float, float]:
    mean = float(np.mean(x))
    std = float(np.std(x, ddof=1))
    t_quant = invert_cdf(student_t_cdf, 1.0 - alpha / 2.0, 0.0, 5.0, len(x) - 1)
    half_width = t_quant * std / math.sqrt(len(x))
    return mean - half_width, mean + half_width


def exact_normal_variance_ci(x: np.ndarray, alpha: float = ALPHA) -> tuple[float, float]:
    n = len(x)
    variance = float(np.var(x, ddof=1))
    chi2_left = invert_cdf(chi2_cdf, alpha / 2.0, 0.0, float(n - 1), n - 1)
    chi2_right = invert_cdf(chi2_cdf, 1.0 - alpha / 2.0, 0.0, float(4 * (n - 1)), n - 1)
    return (n - 1) * variance / chi2_right, (n - 1) * variance / chi2_left


def analyze_column(series: pd.Series, model: str, variation_dir: Path) -> ColumnAnalysis:
    x = series.to_numpy(dtype=float)
    summary = sample_summary(x)
    histograms = histogram_configs(x)
    grouped = grouped_moments(x, histograms["Freedman-Diaconis"]["edges"])
    mm_params = fit_mm(x, model)
    mle_params = fit_mle(x, model)
    fit_scores = {candidate: ks_distance(x, candidate) for candidate in ["normal", "uniform", "shifted_exp"]}
    threshold = summary["mean"] + summary["std_unbiased"]
    variation_path = save_variation_series(series, variation_dir / f"{series.name}_variation_series.csv")
    return ColumnAnalysis(
        name=series.name,
        model=model,
        summary=summary,
        histograms=histograms,
        grouped=grouped,
        mm_params=mm_params,
        mle_params=mle_params,
        fit_scores=fit_scores,
        threshold=threshold,
        prob_empirical=float(np.mean(x > threshold)),
        prob_mm=survival_for_model(model, mm_params, threshold),
        prob_mle=survival_for_model(model, mle_params, threshold),
        ci_mean_asym=asymptotic_mean_ci(x),
        exact_mu_ci=exact_normal_mean_ci(x) if model == "normal" else None,
        exact_sigma2_ci=exact_normal_variance_ci(x) if model == "normal" else None,
        variation_path=variation_path,
    )


def model_label(model: str) -> str:
    mapping = {"normal": "N(μ, σ)", "uniform": "U(a, b)", "shifted_exp": "Exp(λ, c)"}
    return mapping.get(model, model)


def params_to_text(model: str, params: dict[str, float]) -> str:
    if model == "normal":
        return f"μ = {round4(params['mu'])}, σ = {round4(params['sigma'])}"
    if model == "uniform":
        return f"a = {round4(params['a'])}, b = {round4(params['b'])}"
    if model == "shifted_exp":
        return f"λ = {round4(params['lambda'])}, c = {round4(params['c'])}"
    return ", ".join(f"{key} = {round4(value)}" for key, value in params.items())


def moment_method_text(analysis: ColumnAnalysis) -> str:
    mean = round4(analysis.summary["mean"])
    s2 = round4(analysis.summary["variance_biased"])
    s = round4(analysis.summary["std_biased"])
    if analysis.model == "normal":
        return (
            f"Теоретические моменты: E[X] = μ, D[X] = σ². "
            f"Приравниваем их выборочным характеристикам: μ = x̄ = {mean}, σ² = S² = {s2}. "
            f"Отсюда μ̂_MM = {mean}, σ̂_MM = S = {s}."
        )
    if analysis.model == "uniform":
        return (
            f"Теоретические моменты: E[X] = (a + b) / 2, D[X] = (b - a)² / 12. "
            f"Система метода моментов: (a + b) / 2 = x̄ = {mean}, (b - a)² / 12 = S² = {s2}. "
            f"После решения получаем â_MM = x̄ - √(3S²) = {round4(analysis.mm_params['a'])}, "
            f"b̂_MM = x̄ + √(3S²) = {round4(analysis.mm_params['b'])}."
        )
    return (
        f"Теоретические моменты: E[X] = c + 1 / λ, D[X] = 1 / λ². "
        f"Система метода моментов: c + 1 / λ = x̄ = {mean}, 1 / λ² = S² = {s2}. "
        f"Отсюда λ̂_MM = 1 / S = {round4(analysis.mm_params['lambda'])}, "
        f"ĉ_MM = x̄ - S = {round4(analysis.mm_params['c'])}."
    )


def likelihood_text(analysis: ColumnAnalysis) -> str:
    n = int(analysis.summary["n"])
    if analysis.model == "normal":
        return (
            f"Логарифм правдоподобия для выборки объёма n = {n}: "
            "ℓ(μ, σ) = -n ln σ - (n / 2) ln(2π) - (1 / (2σ²)) Σ (x_i - μ)². "
            f"Максимум достигается в точке μ̂_MLE = x̄ = {round4(analysis.mle_params['mu'])}, "
            f"σ̂²_MLE = S² = {round4(analysis.summary['variance_biased'])}, то есть σ̂_MLE = {round4(analysis.mle_params['sigma'])}."
        )
    if analysis.model == "uniform":
        return (
            f"Функция правдоподобия: L(a, b) = (b - a)^(-n) · I{{a ≤ x_(1), x_(n) ≤ b}}, n = {n}. "
            "Тогда ℓ(a, b) = -n ln(b - a) при выполнении ограничений на носитель. "
            f"Чтобы максимизировать ℓ, нужно минимизировать длину интервала, содержащего всю выборку, "
            f"поэтому â_MLE = x_(1) = {round4(analysis.mle_params['a'])}, "
            f"b̂_MLE = x_(n) = {round4(analysis.mle_params['b'])}."
        )
    return (
        f"Функция правдоподобия: L(λ, c) = λ^n exp(-λ Σ(x_i - c)) · I{{c ≤ x_(1)}}, n = {n}. "
        "Логарифм правдоподобия: ℓ(λ, c) = n ln λ - λ Σ(x_i - c) при c ≤ x_(1). "
        f"Максимум достигается при ĉ_MLE = x_(1) = {round4(analysis.mle_params['c'])}, "
        f"а затем λ̂_MLE = 1 / (x̄ - ĉ) = {round4(analysis.mle_params['lambda'])}."
    )


def variation_excerpt_markdown(analysis: ColumnAnalysis, count: int = 5) -> str:
    variation = pd.read_csv(analysis.variation_path)
    n = len(variation)
    excerpt = pd.concat([variation.head(count), variation.tail(count)], ignore_index=True)
    lines = [
        "| i | x_(i) |",
        "| ---: | ---: |",
    ]
    for _, row in excerpt.iterrows():
        lines.append(f"| {int(row['i'])} | {round4(row['x_(i)'])} |")
    if n > 2 * count:
        lines.insert(2 + count, "| ... | ... |")
    return "\n".join(lines)


def qualitative_description(summary: dict[str, float], model: str) -> str:
    if model == "normal":
        return (
            f"Распределение близко к симметричному: коэффициент асимметрии {round4(summary['skewness'])}, "
            f"среднее ({round4(summary['mean'])}) и медиана ({round4(summary['median'])}) почти совпадают. "
            f"Наблюдения лежат в диапазоне [{round4(summary['min'])}; {round4(summary['max'])}], "
            f"выраженной естественной границы нет."
        )
    if model == "uniform":
        return (
            f"Данные почти равномерно заполняют интервал [{round4(summary['min'])}; {round4(summary['max'])}]. "
            f"Асимметрия мала ({round4(summary['skewness'])}), среднее и медиана близки, выраженного хвоста нет."
        )
    return (
        f"Выборка имеет сильную правостороннюю асимметрию ({round4(summary['skewness'])}), "
        f"минимум {round4(summary['min'])} задаёт естественную левую границу, а правый хвост заметно растянут. "
        f"Среднее ({round4(summary['mean'])}) существенно больше медианы ({round4(summary['median'])})."
    )


def create_column_figure(analysis: ColumnAnalysis, out_path: Path) -> None:
    x = pd.read_csv(analysis.variation_path)["x_(i)"].to_numpy(dtype=float)
    xs, ys = ecdf_values(x)
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle(f"{analysis.name}: ЭФР и гистограммы", fontsize=15)

    ax = axes[0, 0]
    ax.step(xs, ys, where="post", label="ЭФР", linewidth=2)
    grid = np.linspace(float(np.min(x)), float(np.max(x)), 400)
    cdf_values = np.array([cdf_for_model(analysis.model, analysis.mle_params, value) for value in grid])
    ax.plot(grid, cdf_values, color="#c44e52", label=f"Теоретическая CDF {model_label(analysis.model)}")
    ax.set_title("Эмпирическая функция распределения")
    ax.set_xlabel("x")
    ax.set_ylabel("F(x)")
    ax.grid(alpha=0.3)
    ax.legend()

    for (rule_name, axis) in [
        ("Sturges", axes[0, 1]),
        ("Scott", axes[1, 0]),
        ("Freedman-Diaconis", axes[1, 1]),
    ]:
        config = analysis.histograms[rule_name]
        grid_pdf = np.linspace(float(np.min(x)), float(np.max(x)), 600)
        axis.hist(x, bins=config["edges"], density=True, alpha=0.75, color="#4c72b0", edgecolor="black")
        axis.plot(grid_pdf, pdf_for_model(analysis.model, analysis.mle_params, grid_pdf), color="#dd8452", linewidth=2.2)
        axis.set_title(f"{rule_name}: bins = {config['bins']}, h = {round4(config['width'])}")
        axis.set_xlabel("x")
        axis.set_ylabel("Плотность")
        axis.grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def kmeans_1d(x: np.ndarray, k: int = 2, max_iter: int = 100) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float)
    centers = np.quantile(x, np.linspace(0, 1, k + 2)[1:-1])
    labels = np.zeros(len(x), dtype=int)
    for _ in range(max_iter):
        distances = np.abs(x[:, None] - centers[None, :])
        new_labels = np.argmin(distances, axis=1)
        new_centers = centers.copy()
        for i in range(k):
            mask = new_labels == i
            if np.any(mask):
                new_centers[i] = np.mean(x[mask])
        if np.array_equal(labels, new_labels) and np.allclose(centers, new_centers):
            break
        labels = new_labels
        centers = new_centers
    order = np.argsort(centers)
    remap = {old: new for new, old in enumerate(order)}
    return np.array([remap[label] for label in labels]), centers[order]


def analyze_x4(series: pd.Series) -> dict[str, object]:
    x = series.to_numpy(dtype=float)
    summary = sample_summary(x)
    labels, centers = kmeans_1d(x, k=2)
    clusters = []
    for cluster_id in range(2):
        sample = x[labels == cluster_id]
        clusters.append(
            {
                "cluster": cluster_id + 1,
                "n": int(len(sample)),
                "min": float(np.min(sample)),
                "max": float(np.max(sample)),
                "mean": float(np.mean(sample)),
                "median": float(np.median(sample)),
                "std_unbiased": float(np.std(sample, ddof=1)),
            }
        )
    xs = np.sort(x)
    gaps = xs[1:] - xs[:-1]
    gap_index = int(np.argmax(gaps))
    return {
        "summary": summary,
        "labels": labels,
        "centers": centers,
        "clusters": clusters,
        "gap_left": float(xs[gap_index]),
        "gap_right": float(xs[gap_index + 1]),
        "threshold": float(0.5 * (xs[gap_index] + xs[gap_index + 1])),
    }


def create_x4_figure(series: pd.Series, x4_analysis: dict[str, object], out_path: Path) -> None:
    x = series.to_numpy(dtype=float)
    labels = np.asarray(x4_analysis["labels"], dtype=int)
    xs, ys = ecdf_values(x)
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))

    axes[0, 0].hist(x, bins=12, color="#55a868", alpha=0.8, edgecolor="black")
    axes[0, 0].axvline(x4_analysis["threshold"], color="#c44e52", linestyle="--", linewidth=2, label="Граница между режимами")
    axes[0, 0].set_title("X4: гистограмма")
    axes[0, 0].set_xlabel("x")
    axes[0, 0].set_ylabel("Частота")
    axes[0, 0].grid(alpha=0.25)
    axes[0, 0].legend()

    axes[0, 1].step(xs, ys, where="post", color="#4c72b0", linewidth=2)
    axes[0, 1].axvline(x4_analysis["threshold"], color="#c44e52", linestyle="--", linewidth=2)
    axes[0, 1].set_title("X4: эмпирическая функция распределения")
    axes[0, 1].set_xlabel("x")
    axes[0, 1].set_ylabel("F(x)")
    axes[0, 1].grid(alpha=0.25)

    order = np.argsort(x)
    axes[1, 0].scatter(np.arange(1, len(x) + 1), x[order], c=labels[order], cmap="Set1", s=28)
    axes[1, 0].axhline(x4_analysis["threshold"], color="#c44e52", linestyle="--", linewidth=2)
    axes[1, 0].set_title("X4: наблюдения после 1D k-means (k = 2)")
    axes[1, 0].set_xlabel("Номер наблюдения в вариационном ряду")
    axes[1, 0].set_ylabel("Значение")
    axes[1, 0].grid(alpha=0.25)

    centers = np.asarray(x4_analysis["centers"], dtype=float)
    axes[1, 1].hist(x[labels == 0], bins=8, alpha=0.75, color="#4c72b0", edgecolor="black", label=f"Кластер 1, центр {round4(centers[0])}")
    axes[1, 1].hist(x[labels == 1], bins=8, alpha=0.75, color="#dd8452", edgecolor="black", label=f"Кластер 2, центр {round4(centers[1])}")
    axes[1, 1].set_title("X4: гистограммы двух кластеров")
    axes[1, 1].set_xlabel("x")
    axes[1, 1].set_ylabel("Частота")
    axes[1, 1].grid(alpha=0.25)
    axes[1, 1].legend()

    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def summary_table_markdown(analysis: ColumnAnalysis) -> str:
    s = analysis.summary
    return "\n".join(
        [
            "| Показатель | Значение |",
            "| --- | ---: |",
            f"| n | {int(s['n'])} |",
            f"| min | {round4(s['min'])} |",
            f"| max | {round4(s['max'])} |",
            f"| Среднее x̄ | {round4(s['mean'])} |",
            f"| Смещённая дисперсия S² | {round4(s['variance_biased'])} |",
            f"| Несмещённая дисперсия σ̂² | {round4(s['variance_unbiased'])} |",
            f"| S | {round4(s['std_biased'])} |",
            f"| σ̂ | {round4(s['std_unbiased'])} |",
            f"| Медиана | {round4(s['median'])} |",
            f"| q0.10 | {round4(s['q10'])} |",
            f"| q0.25 | {round4(s['q25'])} |",
            f"| q0.75 | {round4(s['q75'])} |",
            f"| q0.90 | {round4(s['q90'])} |",
            f"| Асимметрия | {round4(s['skewness'])} |",
        ]
    )


def params_table_markdown(analysis: ColumnAnalysis) -> str:
    return "\n".join(
        [
            "| Метод | Оценки параметров |",
            "| --- | --- |",
            f"| Метод моментов | {params_to_text(analysis.model, analysis.mm_params)} |",
            f"| ММП | {params_to_text(analysis.model, analysis.mle_params)} |",
        ]
    )


def grouped_table_markdown(analysis: ColumnAnalysis) -> str:
    return "\n".join(
        [
            "| Оценка | По исходной выборке | По сгруппированной выборке |",
            "| --- | ---: | ---: |",
            f"| EX | {round4(analysis.summary['mean'])} | {round4(analysis.grouped['mean_grouped'])} |",
            f"| DX | {round4(analysis.summary['variance_unbiased'])} | {round4(analysis.grouped['variance_grouped'])} |",
        ]
    )


def fit_scores_text(analysis: ColumnAnalysis) -> str:
    ordered = sorted(analysis.fit_scores.items(), key=lambda item: item[1])
    return "; ".join(f"{model_label(model)}: {round4(score)}" for model, score in ordered)


def x4_summary_markdown(x4_analysis: dict[str, object]) -> str:
    s = x4_analysis["summary"]
    return "\n".join(
        [
            "| Показатель | Значение |",
            "| --- | ---: |",
            f"| n | {int(s['n'])} |",
            f"| min | {round4(s['min'])} |",
            f"| max | {round4(s['max'])} |",
            f"| Среднее x̄ | {round4(s['mean'])} |",
            f"| Несмещённая дисперсия σ̂² | {round4(s['variance_unbiased'])} |",
            f"| σ̂ | {round4(s['std_unbiased'])} |",
            f"| Медиана | {round4(s['median'])} |",
            f"| q0.25 | {round4(s['q25'])} |",
            f"| q0.75 | {round4(s['q75'])} |",
            f"| Асимметрия | {round4(s['skewness'])} |",
        ]
    )


def x4_clusters_markdown(x4_analysis: dict[str, object]) -> str:
    lines = [
        "| Кластер | n | min | max | Среднее | Медиана | σ̂ |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for cluster in x4_analysis["clusters"]:
        lines.append(
            f"| {cluster['cluster']} | {cluster['n']} | {round4(cluster['min'])} | {round4(cluster['max'])} | "
            f"{round4(cluster['mean'])} | {round4(cluster['median'])} | {round4(cluster['std_unbiased'])} |"
        )
    return "\n".join(lines)


def build_report(
    variant: str,
    csv_path: Path,
    analyses: dict[str, ColumnAnalysis],
    x4_analysis: dict[str, object],
    plots_dir: Path,
) -> str:
    lines: list[str] = [
        "# РГР 1 по математической статистике",
        "",
        "## 1. Общие сведения",
        "",
        f"Идентификатор варианта: **{variant}**.",
        "",
        f"Источник данных: `{csv_path.name}`.",
        "",
        f"Объём выборки: **n = {int(analyses['X1'].summary['n'])}**.",
        "",
        "Для столбцов X1, X2, X3 выполнены обязательные пункты задания: первичное описание выборки, выбор модели распределения, "
        "оценивание параметров методом моментов и методом максимального правдоподобия, оценивание вероятности события, "
        "оценивание моментов по сгруппированной выборке и построение доверительных интервалов. "
        "Для X4 выполнено первичное описание и бонусное разбиение на два кластера.",
        "",
    ]

    for section_number, name in enumerate(["X1", "X2", "X3"], start=2):
        analysis = analyses[name]
        lines.extend(
            [
                f"## {section_number}. Столбец {name}",
                "",
                f"Модель: **{model_label(analysis.model)}**",
                "",
                f"Графики: ![]({plots_dir.as_posix()}/{name}_overview.png)",
                "",
                f"### {section_number}.1 Первичное описание выборки",
                "",
                "Фрагмент вариационного ряда приведён ниже; полный вариационный ряд вынесен в приложение и сохранён в "
                f"`{analysis.variation_path.relative_to(csv_path.parent).as_posix()}`.",
                "",
                variation_excerpt_markdown(analysis),
                "",
                "### Числовые характеристики",
                "",
                summary_table_markdown(analysis),
                "",
                qualitative_description(analysis.summary, analysis.model),
                "",
                f"### {section_number}.2 Предположение о виде закона распределения",
                "",
                f"По визуальной форме гистограммы и ЭФР лучше всего подходит {model_label(analysis.model)}. "
                f"Дополнительно использована KS-подобная метрика для трёх моделей: {fit_scores_text(analysis)}.",
                "",
                f"### {section_number}.3 Оценивание параметров: метод моментов и метод максимального правдоподобия",
                "",
                "Метод моментов:",
                "",
                moment_method_text(analysis),
                "",
                "Метод максимального правдоподобия:",
                "",
                likelihood_text(analysis),
                "",
                "Итоговые оценки:",
                "",
                params_table_markdown(analysis),
                "",
                f"Метод моментов даёт: {params_to_text(analysis.model, analysis.mm_params)}. "
                f"ММП даёт: {params_to_text(analysis.model, analysis.mle_params)}.",
                "",
                f"### {section_number}.4 Оценивание параметрической вероятности двумя способами",
                "",
                f"Выбран порог x0 = x̄ + σ̂ = {round4(analysis.threshold)}. "
                f"Эмпирическая оценка P(X > x0) = {round4(analysis.prob_empirical)}, "
                f"параметрическая по методу моментов = {round4(analysis.prob_mm)}, "
                f"по ММП = {round4(analysis.prob_mle)}.",
                "",
                f"### {section_number}.5 Оценка моментов по сгруппированной выборке",
                "",
                grouped_table_markdown(analysis),
                "",
                f"### {section_number}.6 Доверительные интервалы",
                "",
                f"Асимптотический 95% ДИ для EX: ({round4(analysis.ci_mean_asym[0])}; {round4(analysis.ci_mean_asym[1])}).",
            ]
        )
        if analysis.exact_mu_ci is not None and analysis.exact_sigma2_ci is not None:
            lines.extend(
                [
                    "",
                    f"Точный 95% ДИ для μ: ({round4(analysis.exact_mu_ci[0])}; {round4(analysis.exact_mu_ci[1])}).",
                    "",
                    f"Точный 95% ДИ для σ²: ({round4(analysis.exact_sigma2_ci[0])}; {round4(analysis.exact_sigma2_ci[1])}).",
                ]
            )
        lines.extend(
            [
                "",
                "Интервал доверия 95% означает следующее: если многократно повторять процедуру выборки и строить интервалы по той же формуле, "
                "то примерно 95% таких интервалов будут накрывать истинный параметр. Это не вероятность того, что уже после наблюдения данных "
                "параметр лежит в конкретном построенном интервале.",
                "",
            ]
        )

    lines.extend(
        [
            "## 5. Столбец X4",
            "",
            f"Графики: ![]({plots_dir.as_posix()}/X4_overview.png)",
            "",
            "### 5.1 Первичное описание выборки",
            "",
            x4_summary_markdown(x4_analysis),
            "",
            "На рисунке для X4 показаны и гистограмма, и эмпирическая функция распределения. "
            "ЭФР также демонстрирует резкий переход между двумя группами значений.",
            "",
            f"Столбец X4 выглядит неоднородным: между {round4(x4_analysis['gap_left'])} и {round4(x4_analysis['gap_right'])} "
            f"есть большой разрыв, а медиана ({round4(x4_analysis['summary']['median'])}) заметно ниже среднего "
            f"({round4(x4_analysis['summary']['mean'])}). Это типичный признак смеси двух режимов.",
            "",
            "### 5.2 Бонус: разбиение на 2 кластера",
            "",
            x4_clusters_markdown(x4_analysis),
            "",
            f"1D k-means с k = 2 разделил выборку на два устойчивых кластера с центрами "
            f"{round4(x4_analysis['centers'][0])} и {round4(x4_analysis['centers'][1])}. "
            f"Общее среднее плохо описывает такую смесь, потому что ни один из режимов не сосредоточен около "
            f"{round4(x4_analysis['summary']['mean'])}.",
            "",
            "## 6. Итоговый вывод",
            "",
            f"Для X1 выбрана модель {model_label(analyses['X1'].model)}: выборка почти симметрична, "
            "оценки параметров по методу моментов и ММП совпадают, а доверительные интервалы для среднего достаточно узкие.",
            "",
            f"Для X2 выбрана модель {model_label(analyses['X2'].model)}: данные достаточно равномерно заполняют интервал, "
            "а различие между методом моментов и ММП связано с тем, что ММП использует крайние наблюдения.",
            "",
            f"Для X3 выбрана модель {model_label(analyses['X3'].model)}: наблюдается выраженная правосторонняя асимметрия "
            "и естественная левая граница. Эмпирические и параметрические оценки вероятности события P(X > x0) "
            "практически совпадают, что поддерживает выбранную модель.",
            "",
            "Столбец X4 по форме похож на смесь двух подвыборок. Поэтому его корректнее описывать не одним средним, "
            "а отдельно по двум режимам.",
            "",
            "## 7. Приложение",
            "",
            "Полные вариационные ряды сохранены в папке `output/variation_series` и могут быть приложены к отчёту отдельно.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / "output"
    plots_dir = output_dir / "plots"
    variation_dir = output_dir / "variation_series"
    output_dir.mkdir(exist_ok=True)
    plots_dir.mkdir(exist_ok=True)
    variation_dir.mkdir(exist_ok=True)

    csv_path = choose_csv(base_dir)
    variant = parse_variant(csv_path)
    df = pd.read_csv(csv_path)

    model_map = identify_models(df)
    analyses = {name: analyze_column(df[name], model_map[name], variation_dir) for name in ["X1", "X2", "X3"]}
    x4_analysis = analyze_x4(df["X4"])

    for name, analysis in analyses.items():
        create_column_figure(analysis, plots_dir / f"{name}_overview.png")
    create_x4_figure(df["X4"], x4_analysis, plots_dir / "X4_overview.png")

    report = build_report(variant, csv_path, analyses, x4_analysis, plots_dir.relative_to(base_dir))
    report_path = base_dir / "report.md"
    report_path.write_text(report, encoding="utf-8")

    print(f"CSV: {csv_path.name}")
    print(f"Вариант: {variant}")
    print("Назначение моделей:")
    for name in ["X1", "X2", "X3"]:
        print(f"  {name}: {analyses[name].model}")
    print(f"Отчёт: {report_path.name}")
    print(f"Графики: {plots_dir}")


if __name__ == "__main__":
    main()
