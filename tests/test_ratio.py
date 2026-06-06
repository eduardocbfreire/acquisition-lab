"""Bloco 5 — métricas de razão (delta method)."""

import numpy as np
import pytest

from acquisition_lab.analysis.ratio import average_order_value
from acquisition_lab.analysis.stats import bootstrap_ratio, ratio_delta_method
from acquisition_lab.ingest import load_example


def test_ratio_point_estimate():
    x = np.array([10.0, 20.0, 30.0, 40.0])
    y = np.array([1.0, 2.0, 3.0, 4.0])
    res = ratio_delta_method(x, y)
    assert res.ratio == pytest.approx(100 / 10)  # sum(x)/sum(y)


def test_covariance_term_changes_variance():
    # Numerador e denominador positivamente correlacionados: o delta method
    # (com covariância) NÃO deve coincidir com o ingênuo (denominador constante).
    rng = np.random.default_rng(0)
    y = rng.poisson(3, size=500).astype(float) + 1
    x = y * 70 + rng.normal(0, 50, size=500)  # receita cresce com pedidos
    res = ratio_delta_method(x, y)
    assert res.cov_xy > 0
    assert res.var != pytest.approx(res.var_naive, rel=1e-3)


def test_delta_method_agrees_with_bootstrap():
    rng = np.random.default_rng(1)
    y = rng.poisson(2, size=2000).astype(float) + 1
    x = y * 60 + rng.normal(0, 40, size=2000)
    res = ratio_delta_method(x, y)
    point, lo, hi = bootstrap_ratio(x, y, n_boot=4000, seed=2)
    # Largura dos IC deve bater de forma aproximada (validação cruzada).
    delta_width = res.hi - res.lo
    boot_width = hi - lo
    assert boot_width == pytest.approx(delta_width, rel=0.25)


def test_raises_on_mismatched_length():
    with pytest.raises(ValueError):
        ratio_delta_method(np.array([1.0, 2.0]), np.array([1.0]))


def test_runs_on_example_sales():
    df = load_example("sales")
    res = average_order_value(df, run_bootstrap=True, n_boot=2000)
    assert res.estimate.ratio > 0
    assert res.estimate.lo < res.estimate.ratio < res.estimate.hi
    assert res.bootstrap is not None
    # Delta method e bootstrap próximos no ponto.
    assert res.bootstrap[0] == pytest.approx(res.estimate.ratio, rel=0.02)
