"""Bloco 1 — Change points.

PELT (Pruned Exact Linear Time) via ``ruptures``, modo offline, segmentação
múltipla. Penalidade estilo BIC, proporcional a log(n):

    beta = k * d * sigma2 * log(n)

onde d = nº de dimensões (1 para univariada), sigma2 é a variância do ruído
estimada de forma robusta pela MAD dos primeiros diffs, n é o tamanho da série
e k é o multiplicador (padrão 1.0).

Defesas contra excesso de pontos: penalidade BIC, ``min_size``, filtro de
magnitude mínima (descarta quebras com salto de média < 1 MAD) e teste de
estabilidade (re-roda com k=1.5 e mantém só os pontos que persistem).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
import ruptures as rpt

from .stats import robust_sigma2_from_diffs

MIN_SERIES_LENGTH = 30  # série mínima antes de habilitar a detecção


@dataclass(frozen=True)
class Segment:
    start: int  # índice inicial (inclusive)
    end: int  # índice final (exclusivo)
    mean: float


@dataclass(frozen=True)
class ChangePointResult:
    indices: list[int]  # change points finais (persistentes e acima do limiar)
    segments: list[Segment]
    penalty: float
    sigma2: float
    mad_diffs: float
    model: str
    min_size: int
    k: float
    n: int
    dropped_low_magnitude: list[int] = field(default_factory=list)
    dropped_unstable: list[int] = field(default_factory=list)
    enabled: bool = True
    message: str = ""


def _segment_means(signal: np.ndarray, bkps: list[int]) -> list[Segment]:
    segments = []
    prev = 0
    for b in bkps:
        seg = signal[prev:b]
        segments.append(Segment(prev, b, float(np.mean(seg)) if seg.size else float("nan")))
        prev = b
    return segments


def _predict(signal: np.ndarray, model: str, min_size: int, jump: int, pen: float) -> list[int]:
    algo = rpt.Pelt(model=model, min_size=min_size, jump=jump).fit(signal)
    bkps = algo.predict(pen=pen)  # inclui n no final
    return [b for b in bkps if b < len(signal)]  # mantém só change points interiores


def detect_change_points(
    series: np.ndarray,
    *,
    model: str = "l2",
    min_size: int = 7,
    jump: int = 1,
    k: float = 1.0,
    min_magnitude_mad: float = 1.0,
    stability_k: float = 1.5,
    detrend: bool = False,
) -> ChangePointResult:
    """Detecta change points de NÍVEL por PELT com penalidade BIC.

    Parâmetros padrão da spec: ``model="l2"`` (nível/média), ``min_size=7``
    (diário; use 4 para semanal), ``jump=1``, penalidade derivada de ``k=1.0``,
    ``sigma2`` por MAD e escala ``log(n)``. ``model="normal"`` detecta mudança
    de variância e ``model="linear"`` mudança de tendência.

    Para séries com tendência forte, passe ``detrend=True`` (remove tendência
    linear por mínimos quadrados antes do l2) ou use ``model="linear"``, para
    não confundir tendência suave com quebra de nível.

    Filtros: descarta quebras cujo salto de média seja menor que
    ``min_magnitude_mad`` MAD; e mantém apenas pontos que persistem ao re-rodar
    com ``stability_k`` (padrão 1.5).
    """
    signal = np.asarray(series, dtype=float).ravel()
    n = signal.size

    if n < MIN_SERIES_LENGTH:
        return ChangePointResult(
            indices=[],
            segments=[Segment(0, n, float(np.mean(signal)) if n else float("nan"))],
            penalty=float("nan"),
            sigma2=float("nan"),
            mad_diffs=float("nan"),
            model=model,
            min_size=min_size,
            k=k,
            n=n,
            enabled=False,
            message=f"série com {n} pontos; mínimo de {MIN_SERIES_LENGTH} para habilitar a detecção",
        )

    work = signal.copy()
    if detrend:
        t = np.arange(n)
        coef = np.polyfit(t, work, 1)
        work = work - np.polyval(coef, t)

    sigma2, mad_diffs = robust_sigma2_from_diffs(work)
    if not math.isfinite(sigma2) or sigma2 <= 0:
        sigma2 = float(np.var(work)) or 1.0
    d = 1  # univariada

    def beta(mult: float) -> float:
        return mult * d * sigma2 * math.log(n)

    pen = beta(k)
    raw_bkps = _predict(work, model, min_size, jump, pen)

    # Filtro de magnitude: salto de média entre segmentos vizinhos >= limiar.
    threshold = min_magnitude_mad * mad_diffs if math.isfinite(mad_diffs) else 0.0
    bounds = [0] + raw_bkps + [n]
    kept: list[int] = []
    dropped_low: list[int] = []
    for i, bkp in enumerate(raw_bkps):
        left = signal[bounds[i] : bounds[i + 1]]
        right = signal[bounds[i + 1] : bounds[i + 2]]
        jump_mag = abs(float(np.mean(right)) - float(np.mean(left)))
        if jump_mag >= threshold:
            kept.append(bkp)
        else:
            dropped_low.append(bkp)

    # Teste de estabilidade: re-roda com k mais alto e mantém pontos próximos.
    stable_bkps = _predict(work, model, min_size, jump, beta(stability_k))
    persistent: list[int] = []
    dropped_unstable: list[int] = []
    for bkp in kept:
        if any(abs(bkp - s) <= min_size for s in stable_bkps):
            persistent.append(bkp)
        else:
            dropped_unstable.append(bkp)

    segments = _segment_means(signal, persistent + [n])
    return ChangePointResult(
        indices=persistent,
        segments=segments,
        penalty=pen,
        sigma2=sigma2,
        mad_diffs=mad_diffs,
        model=model,
        min_size=min_size,
        k=k,
        n=n,
        dropped_low_magnitude=dropped_low,
        dropped_unstable=dropped_unstable,
        enabled=True,
        message="ok",
    )
