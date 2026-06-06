"""Bloco 4 — Mídia vs resultado.

CAC(t) = gasto no período t / aquisições atribuídas ao período t, agregado por
semana, com defasagem fixa entre gasto e conversão. A mesma detecção de change
points do bloco 1 roda sobre a série de CAC.

Defasagem: conversões atrasam em relação ao gasto. Estimamos por correlação
cruzada (teto de 30 dias) e deslocamos as aquisições para trás antes de dividir.
A defasagem usada é sempre reportada.

CUIDADO CENTRAL E INEGOCIÁVEL: atribuição não é incrementalidade. O CAC daqui é
DESCRITIVO, não causal — está contaminado por confundimento (demanda e
sazonalidade movem tanto o gasto quanto as conversões). Medir incrementalidade
exige experimento geográfico ou controle sintético, fora do escopo de uma
análise descritiva de CSV.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .changepoints import ChangePointResult, detect_change_points

# Rótulo exibido em todo lugar que mostra CAC. Não remova nem suavize.
CAC_DESCRIPTIVE_DISCLAIMER = (
    "CAC descritivo, não causal: calculado de conversões atribuídas e "
    "contaminado por confundimento (demanda e sazonalidade movem gasto e "
    "conversões juntos). Medir incrementalidade exige experimento geográfico "
    "ou controle sintético — fora do escopo de uma análise descritiva de CSV."
)

MAX_LAG_DAYS = 30


@dataclass(frozen=True)
class CacResult:
    weekly: pd.DataFrame  # colunas: week, spend, conversions, cac, cac_smooth
    lag_days: int
    change_points: ChangePointResult
    change_point_weeks: list[pd.Timestamp]
    disclaimer: str = CAC_DESCRIPTIVE_DISCLAIMER


def estimate_lag(spend: np.ndarray, conversions: np.ndarray, max_lag: int = MAX_LAG_DAYS) -> int:
    """Estima a defasagem (em dias) das conversões em relação ao gasto.

    Correlação cruzada com teto de ``max_lag``: para cada candidato L >= 0,
    correlaciona ``spend[:-L]`` com ``conversions[L:]`` (conversões atrasadas em
    L). Devolve o L com maior correlação. Como conversões atrasam o gasto, L é
    sempre não-negativo.
    """
    spend = np.asarray(spend, dtype=float)
    conv = np.asarray(conversions, dtype=float)
    n = spend.size
    max_lag = min(max_lag, n - 5)
    best_lag, best_corr = 0, -np.inf
    for lag in range(0, max_lag + 1):
        a = spend[: n - lag]
        b = conv[lag:]
        if a.size < 5 or np.std(a) == 0 or np.std(b) == 0:
            continue
        corr = float(np.corrcoef(a, b)[0, 1])
        if corr > best_corr:
            best_corr, best_lag = corr, lag
    return best_lag


def compute_cac(
    df: pd.DataFrame,
    *,
    lag_days: int | None = None,
    smooth_weeks: int = 4,
    min_size: int = 4,
    detect: bool = True,
) -> CacResult:
    """Calcula CAC semanal com defasagem e detecção de change points.

    ``df`` diário com colunas ``date``, ``spend``, ``conversions``. As
    conversões são deslocadas para trás pela defasagem estimada (ou ``lag_days``
    fornecido) antes da agregação semanal, para alinhar gasto e resultado.
    CAC = gasto semanal / conversões alinhadas da semana. A detecção de change
    points (bloco 1, ``min_size=4`` para semanal) roda sobre a série de CAC.
    """
    required = {"date", "spend", "conversions"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"mídia exige {sorted(required)}; faltam {sorted(missing)}")

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    spend = df["spend"].to_numpy(dtype=float)
    conv = df["conversions"].to_numpy(dtype=float)

    if lag_days is None:
        lag_days = estimate_lag(spend, conv)

    # Desloca conversões para trás pela defasagem: aquisição[t] passa a ser
    # atribuída ao gasto de t-lag, então alinhamos conv[t+lag] com spend[t].
    aligned_conv = np.full_like(conv, np.nan)
    if lag_days > 0:
        aligned_conv[: len(conv) - lag_days] = conv[lag_days:]
    else:
        aligned_conv = conv.copy()
    df["aligned_conversions"] = aligned_conv

    # Agregação semanal (semana âncora na segunda-feira).
    df["week"] = df["date"].dt.to_period("W").dt.start_time
    weekly = (
        df.groupby("week")
        .agg(spend=("spend", "sum"), conversions=("aligned_conversions", "sum"))
        .reset_index()
    )
    # Semanas incompletas no fim (sem conversões alinhadas) são descartadas.
    weekly = weekly[weekly["conversions"] > 0].reset_index(drop=True)
    weekly["cac"] = weekly["spend"] / weekly["conversions"]
    weekly["cac_smooth"] = (
        weekly["cac"].rolling(window=smooth_weeks, min_periods=1, center=True).mean()
    )

    if detect:
        cp = detect_change_points(weekly["cac"].to_numpy(), model="l2", min_size=min_size)
    else:
        cp = detect_change_points(np.array([]), min_size=min_size)
    cp_weeks = [weekly["week"].iloc[i] for i in cp.indices if i < len(weekly)]

    return CacResult(
        weekly=weekly,
        lag_days=int(lag_days),
        change_points=cp,
        change_point_weeks=cp_weeks,
    )
