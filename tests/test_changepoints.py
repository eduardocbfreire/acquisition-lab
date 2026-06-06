"""Bloco 1 — change points."""

import numpy as np

from acquisition_lab.analysis.changepoints import MIN_SERIES_LENGTH, detect_change_points


def test_detects_planted_level_shift():
    rng = np.random.default_rng(0)
    a = rng.normal(10, 1.0, size=60)
    b = rng.normal(20, 1.0, size=60)  # degrau claro de nível
    signal = np.concatenate([a, b])
    res = detect_change_points(signal, model="l2")
    assert res.enabled
    assert len(res.indices) >= 1
    # O change point deve cair perto do ponto plantado (índice 60).
    assert any(abs(i - 60) <= 5 for i in res.indices)


def test_pure_noise_yields_few_or_no_changepoints():
    rng = np.random.default_rng(1)
    signal = rng.normal(0, 1.0, size=120)
    res = detect_change_points(signal, model="l2")
    # Penalidade BIC + magnitude + estabilidade devem evitar excesso de pontos.
    assert len(res.indices) <= 1


def test_disabled_below_minimum_length():
    res = detect_change_points(np.arange(MIN_SERIES_LENGTH - 1, dtype=float))
    assert res.enabled is False
    assert res.indices == []


def test_magnitude_filter_drops_tiny_jumps():
    rng = np.random.default_rng(2)
    # Salto minúsculo em relação ao ruído não deve sobreviver ao filtro.
    a = rng.normal(10, 2.0, size=60)
    b = rng.normal(10.2, 2.0, size=60)
    signal = np.concatenate([a, b])
    res = detect_change_points(signal, model="l2")
    assert len(res.indices) == 0


def test_higher_k_is_more_conservative():
    rng = np.random.default_rng(3)
    signal = np.concatenate([rng.normal(0, 1, 40), rng.normal(5, 1, 40), rng.normal(0, 1, 40)])
    loose = detect_change_points(signal, k=1.0)
    strict = detect_change_points(signal, k=3.0)
    assert len(strict.indices) <= len(loose.indices)
