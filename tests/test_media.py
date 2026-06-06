"""Bloco 4 — mídia vs resultado."""

import numpy as np

from acquisition_lab.analysis.media import (
    CAC_DESCRIPTIVE_DISCLAIMER,
    compute_cac,
    estimate_lag,
)
from acquisition_lab.ingest import load_example


def test_estimate_lag_recovers_planted_lag():
    # Conversões = gasto defasado em 7 dias.
    rng = np.random.default_rng(0)
    n, lag = 180, 7
    spend = 1000 + 200 * np.sin(np.arange(n) * 2 * np.pi / 7) + rng.normal(0, 20, n)
    conv = np.zeros(n)
    for i in range(n):
        conv[i] = spend[max(0, i - lag)] / 40.0
    est = estimate_lag(spend, conv, max_lag=30)
    assert abs(est - lag) <= 1


def test_lag_capped_at_30():
    df = load_example("media")
    res = compute_cac(df)
    assert 0 <= res.lag_days <= 30


def test_detects_planted_cac_change_point():
    df = load_example("media")
    res = compute_cac(df, smooth_weeks=4, min_size=4)
    assert res.change_points.enabled
    # Há um change point plantado no CAC (degrau ~dia 115).
    assert len(res.change_points.indices) >= 1


def test_disclaimer_present_and_unmodified():
    df = load_example("media")
    res = compute_cac(df)
    assert res.disclaimer == CAC_DESCRIPTIVE_DISCLAIMER
    assert "não causal" in res.disclaimer
    assert "incrementalidade" in res.disclaimer


def test_cac_is_positive():
    df = load_example("media")
    res = compute_cac(df)
    assert (res.weekly["cac"] > 0).all()
