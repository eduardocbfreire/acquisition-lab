"""Helpers estatísticos transversais.

Princípio da spec: toda taxa é proporção ou razão, e a incerteza precisa ser
reportada de forma honesta (intervalo + n absoluto). Estes helpers centralizam
isso para funil, coorte e métricas de razão não duplicarem método.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from statsmodels.stats.proportion import proportion_confint


@dataclass(frozen=True)
class ProportionEstimate:
    """Proporção com intervalo de Wilson e o n absoluto ao lado."""

    rate: float
    lo: float
    hi: float
    count: int
    nobs: int

    @property
    def n(self) -> int:
        return self.nobs


def wilson_proportion(count: int, nobs: int, alpha: float = 0.05) -> ProportionEstimate:
    """Proporção com IC de Wilson (score), nível 1 - ``alpha``.

    Usa ``statsmodels.stats.proportion.proportion_confint(method="wilson")``,
    nunca Wald. Reporta sempre o n absoluto. Com ``nobs == 0`` devolve NaN.
    """
    count = int(count)
    nobs = int(nobs)
    if nobs <= 0:
        return ProportionEstimate(float("nan"), float("nan"), float("nan"), count, nobs)
    rate = count / nobs
    lo, hi = proportion_confint(count, nobs, alpha=alpha, method="wilson")
    return ProportionEstimate(rate, float(lo), float(hi), count, nobs)


def mad(values: np.ndarray) -> float:
    """Desvio absoluto mediano (MAD) bruto, sem fator de consistência."""
    values = np.asarray(values, dtype=float)
    if values.size == 0:
        return float("nan")
    return float(np.median(np.abs(values - np.median(values))))


def robust_sigma2_from_diffs(series: np.ndarray) -> tuple[float, float]:
    """Variância do ruído estimada de forma robusta pela MAD dos primeiros diffs.

    Retorna ``(sigma2, mad_diffs)``. O fator 1.4826 converte MAD em desvio
    padrão sob normalidade; ``sigma2`` é esse desvio ao quadrado. ``mad_diffs``
    (bruto) é devolvido para servir de unidade no filtro de magnitude do PELT.
    """
    series = np.asarray(series, dtype=float)
    if series.size < 2:
        return float("nan"), float("nan")
    diffs = np.diff(series)
    mad_diffs = mad(diffs)
    sigma = 1.4826 * mad_diffs
    return float(sigma**2), float(mad_diffs)


@dataclass(frozen=True)
class RatioEstimate:
    """Razão R = X/Y com variância pelo delta method."""

    ratio: float
    var: float
    se: float
    lo: float
    hi: float
    n_units: int
    cov_xy: float
    # Variância ingênua (denominador tratado como constante), só para contraste.
    var_naive: float

    @property
    def se_naive(self) -> float:
        return float(np.sqrt(self.var_naive)) if self.var_naive >= 0 else float("nan")


def ratio_delta_method(
    numerator: np.ndarray, denominator: np.ndarray, z: float = 1.96
) -> RatioEstimate:
    """Razão R = sum(X)/sum(Y) com variância pelo delta method.

    A unidade de ``numerator``/``denominator`` é a unidade de agregação (ex.:
    um valor por usuário). O denominador é variável aleatória; a fórmula
    considera variância do numerador, do denominador E a covariância:

        var(R) ≈ (1 / mean_y**2) * (var_x - 2*R*cov_xy + R**2 * var_y) / n

    IC 95% como R ± 1.96 * sqrt(var(R)). Devolve também ``var_naive``, que
    trata o denominador como constante (ignora ``var_y`` e a covariância),
    apenas para contraste. Esse atalho é enviesado e pode super OU subestimar
    a incerteza dependendo do sinal/magnitude da covariância — com correlação
    positiva forte, o delta method costuma dar um IC mais ESTREITO que o ingênuo.
    """
    x = np.asarray(numerator, dtype=float)
    y = np.asarray(denominator, dtype=float)
    if x.shape != y.shape:
        raise ValueError("numerator e denominator precisam ter o mesmo tamanho")
    n = x.size
    if n < 2:
        raise ValueError("delta method precisa de ao menos 2 unidades")

    mean_x = float(np.mean(x))
    mean_y = float(np.mean(y))
    if mean_y == 0:
        raise ValueError("média do denominador é zero; razão indefinida")

    ratio = mean_x / mean_y
    # Variâncias/covariância amostrais (ddof=1) na unidade de agregação.
    var_x = float(np.var(x, ddof=1))
    var_y = float(np.var(y, ddof=1))
    cov_xy = float(np.cov(x, y, ddof=1)[0, 1])

    var = (1.0 / mean_y**2) * (var_x - 2.0 * ratio * cov_xy + ratio**2 * var_y) / n
    var = max(var, 0.0)
    se = float(np.sqrt(var))

    # Ingênuo: denominador constante => var(R) ~ var_x / (n * mean_y**2).
    var_naive = (1.0 / mean_y**2) * var_x / n

    return RatioEstimate(
        ratio=ratio,
        var=var,
        se=se,
        lo=ratio - z * se,
        hi=ratio + z * se,
        n_units=n,
        cov_xy=cov_xy,
        var_naive=var_naive,
    )


def bootstrap_ratio(
    numerator: np.ndarray,
    denominator: np.ndarray,
    n_boot: int = 10000,
    seed: int = 0,
    alpha: float = 0.05,
) -> tuple[float, float, float]:
    """Bootstrap da razão reamostrando a unidade de agregação inteira.

    Validação OPCIONAL do delta method (não é o método primário). Reamostra
    pares (X_i, Y_i) com reposição ``n_boot`` vezes e devolve
    ``(ponto, lo, hi)`` pelos percentis.
    """
    x = np.asarray(numerator, dtype=float)
    y = np.asarray(denominator, dtype=float)
    n = x.size
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(n_boot, n))
    sums_x = x[idx].sum(axis=1)
    sums_y = y[idx].sum(axis=1)
    ratios = sums_x / sums_y
    point = float(x.sum() / y.sum())
    lo, hi = np.quantile(ratios, [alpha / 2, 1 - alpha / 2])
    return point, float(lo), float(hi)
