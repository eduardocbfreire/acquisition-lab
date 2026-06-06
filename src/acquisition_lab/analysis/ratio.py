"""Bloco 5 — Métricas de razão (delta method).

Aplicado na análise de vendas: o ticket médio (AOV = receita total / pedidos
totais) é uma razão X/Y onde o denominador (pedidos) é variável aleatória e
positivamente correlacionado com o numerador (receita). A variância vem do
delta method, com o termo de covariância — calculada na unidade de agregação
correta (o usuário). Bootstrap reamostrando usuários inteiros como validação
opcional.

O núcleo numérico vive em ``stats.ratio_delta_method`` /
``stats.bootstrap_ratio_samples``; aqui ficam os atalhos voltados ao DataFrame de vendas.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .stats import RatioEstimate, bootstrap_ratio_samples, ratio_delta_method


@dataclass(frozen=True)
class AovResult:
    estimate: RatioEstimate
    bootstrap: tuple[float, float, float] | None  # (ponto, lo, hi) se solicitado
    bootstrap_samples: np.ndarray | None  # distribuição reamostrada (para o gráfico)
    numerator_label: str
    denominator_label: str


def per_user_ticket(
    df: pd.DataFrame, *, numerator: str = "revenue", denominator: str = "orders"
) -> np.ndarray:
    """Ticket de cada usuário com pelo menos 1 pedido (receita/pedidos).

    Unidade do histograma de distribuição: o ticket individual, não o agregado.
    Usuários sem pedido ficam de fora (divisão indefinida)."""
    for col in (numerator, denominator):
        if col not in df.columns:
            raise ValueError(f"coluna '{col}' ausente no DataFrame de vendas")
    mask = df[denominator] > 0
    return (df.loc[mask, numerator] / df.loc[mask, denominator]).to_numpy(dtype=float)


def average_order_value(
    df: pd.DataFrame,
    *,
    numerator: str = "revenue",
    denominator: str = "orders",
    run_bootstrap: bool = False,
    n_boot: int = 10000,
    seed: int = 0,
) -> AovResult:
    """Ticket médio (receita/pedidos) com IC pelo delta method.

    ``df`` tem uma linha por usuário (unidade de agregação) com as colunas de
    receita e de pedidos. A razão é ``sum(receita)/sum(pedidos)``; a variância
    considera a covariância entre receita e pedidos por usuário. ``run_bootstrap``
    liga a validação opcional reamostrando usuários inteiros.
    """
    for col in (numerator, denominator):
        if col not in df.columns:
            raise ValueError(f"coluna '{col}' ausente no DataFrame de vendas")

    x = df[numerator].to_numpy(dtype=float)
    y = df[denominator].to_numpy(dtype=float)

    estimate = ratio_delta_method(x, y)
    boot = None
    samples = None
    if run_bootstrap:
        samples = bootstrap_ratio_samples(x, y, n_boot=n_boot, seed=seed)
        point = float(x.sum() / y.sum())
        lo, hi = np.quantile(samples, [0.025, 0.975])
        boot = (point, float(lo), float(hi))

    return AovResult(
        estimate=estimate,
        bootstrap=boot,
        bootstrap_samples=samples,
        numerator_label=numerator,
        denominator_label=denominator,
    )
