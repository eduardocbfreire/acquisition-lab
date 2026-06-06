"""Bloco 3 — Coorte / retenção.

Coorte definida pelo período de aquisição (semana de signup como padrão).
Retenção medida em períodos relativos desde a aquisição. A matriz é triangular
(coortes recentes têm menos períodos observados) e células ausentes NÃO são
imputadas. Cada célula reporta taxa, n da coorte e IC de Wilson 95%.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .stats import wilson_proportion


@dataclass(frozen=True)
class RetentionMatrix:
    rates: pd.DataFrame  # index=coorte, columns=período relativo; NaN = não observado
    counts: pd.DataFrame  # retidos_n por célula
    ci_low: pd.DataFrame
    ci_high: pd.DataFrame
    cohort_sizes: pd.Series  # tamanho de cada coorte
    granularity: str
    max_period: int


def build_retention_matrix(
    df: pd.DataFrame,
    *,
    granularity: str = "W",
    max_period: int = 12,
    alpha: float = 0.05,
    observation_end: pd.Timestamp | None = None,
) -> RetentionMatrix:
    """Constrói a matriz de retenção relativa à aquisição.

    ``df`` com colunas ``user_id``, ``signup_date``, ``activity_date``. A
    coorte é o período (semana por padrão) do signup; o período relativo n é a
    diferença, em períodos, entre a atividade e o signup. ``célula =
    retidos_n / tamanho_da_coorte``, onde retido = fez o evento qualificador
    (uma linha de atividade) no período n.

    Triangularidade: para cada coorte só preenchemos períodos já maduros
    (período <= idade observável da coorte). Os demais ficam NaN — sem
    imputação. Não se deve comparar células de maturidades diferentes.
    """
    required = {"user_id", "signup_date", "activity_date"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"coorte exige {sorted(required)}; faltam {sorted(missing)}")
    if granularity not in {"W", "M"}:
        raise ValueError("granularity deve ser 'W' (semana) ou 'M' (mês)")

    df = df.copy()
    df["signup_date"] = pd.to_datetime(df["signup_date"])
    df["activity_date"] = pd.to_datetime(df["activity_date"])
    if observation_end is None:
        observation_end = df["activity_date"].max()

    period_days = {"W": 7, "M": 30}[granularity]

    # Coorte: âncora do período de signup (início do período).
    df["cohort"] = df["signup_date"].dt.to_period(granularity).dt.start_time
    # Período relativo (inteiro) desde o signup.
    delta_days = (df["activity_date"] - df["signup_date"]).dt.days
    df["period"] = (delta_days // period_days).astype(int)
    df = df[(df["period"] >= 0) & (df["period"] <= max_period)]

    # Tamanho da coorte = usuários únicos por coorte de signup.
    cohort_sizes = df.groupby("cohort")["user_id"].nunique().sort_index().rename("cohort_size")

    # Retidos por (coorte, período) = usuários únicos com atividade no período.
    retained = df.groupby(["cohort", "period"])["user_id"].nunique().rename("retained")
    retained = retained.reset_index()

    cohorts = list(cohort_sizes.index)
    periods = list(range(max_period + 1))
    rates = pd.DataFrame(index=cohorts, columns=periods, dtype=float)
    counts = pd.DataFrame(index=cohorts, columns=periods, dtype=float)
    ci_low = pd.DataFrame(index=cohorts, columns=periods, dtype=float)
    ci_high = pd.DataFrame(index=cohorts, columns=periods, dtype=float)

    retained_map = {(r.cohort, int(r.period)): int(r.retained) for r in retained.itertuples()}

    for cohort in cohorts:
        size = int(cohort_sizes[cohort])
        # Maturidade: quantos períodos completos já se passaram para esta coorte.
        max_obs = int((observation_end - cohort).days // period_days)
        max_obs = min(max_obs, max_period)
        for p in periods:
            if p > max_obs:
                continue  # não observado -> permanece NaN (sem imputar)
            cnt = retained_map.get((cohort, p), 0)
            est = wilson_proportion(cnt, size, alpha=alpha)
            rates.loc[cohort, p] = est.rate
            counts.loc[cohort, p] = cnt
            ci_low.loc[cohort, p] = est.lo
            ci_high.loc[cohort, p] = est.hi

    return RetentionMatrix(
        rates=rates,
        counts=counts,
        ci_low=ci_low,
        ci_high=ci_high,
        cohort_sizes=cohort_sizes,
        granularity=granularity,
        max_period=max_period,
    )
