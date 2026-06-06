"""Bloco 2 — funil."""

import pandas as pd
import pytest

from acquisition_lab.analysis.funnel import compute_funnel, infer_step_order
from acquisition_lab.ingest import load_example


def _toy_funnel():
    # 100 entram (visit), 50 signup, 25 purchase. Tempos bem dentro da janela.
    rows = []
    base = pd.Timestamp("2026-01-01")
    for i in range(100):
        rows.append((f"u{i}", "visit", base))
        if i < 50:
            rows.append((f"u{i}", "signup", base + pd.Timedelta(hours=1)))
        if i < 25:
            rows.append((f"u{i}", "purchase", base + pd.Timedelta(hours=2)))
    return pd.DataFrame(rows, columns=["user_id", "step", "event_time"])


def test_step_conversion_counts_unique_users():
    df = _toy_funnel()
    res = compute_funnel(
        df,
        ["visit", "signup", "purchase"],
        window_end=pd.Timestamp("2026-03-01"),
        maturation_days=14,
    )
    signup = res.steps[1]
    assert signup.users == 50
    assert signup.step_conversion.count == 50
    assert signup.step_conversion.nobs == 100
    assert signup.step_conversion.rate == pytest.approx(0.5)


def test_end_to_end_is_direct_not_product_of_steps():
    df = _toy_funnel()
    res = compute_funnel(
        df,
        ["visit", "signup", "purchase"],
        window_end=pd.Timestamp("2026-03-01"),
        maturation_days=14,
    )
    # Ponta a ponta = 25/100 direto sobre entrada e saída.
    assert res.end_to_end.rate == pytest.approx(0.25)
    assert res.end_to_end.count == 25
    assert res.end_to_end.nobs == 100


def test_wilson_interval_is_not_wald():
    # Para p=0.5, n=100, Wilson não é simétrico em torno de p como o Wald
    # ingênuo (p ± z*sqrt(p(1-p)/n) daria [0.402, 0.598]).
    df = _toy_funnel()
    res = compute_funnel(
        df,
        ["visit", "signup", "purchase"],
        window_end=pd.Timestamp("2026-03-01"),
        maturation_days=14,
    )
    est = res.steps[1].step_conversion
    assert 0 < est.lo < est.rate < est.hi < 1
    # Wilson para 50/100 ~ [0.404, 0.596]: largura próxima mas centro deslocado.
    assert est.lo == pytest.approx(0.4038, abs=1e-3)
    assert est.hi == pytest.approx(0.5962, abs=1e-3)


def test_partial_cohorts_excluded():
    df = _toy_funnel()
    # Adiciona 20 usuários que entraram ontem (imaturos) e não converteram.
    recent = pd.Timestamp("2026-02-28")
    extra = [(f"r{i}", "visit", recent) for i in range(20)]
    df = pd.concat([df, pd.DataFrame(extra, columns=df.columns)], ignore_index=True)
    res = compute_funnel(
        df,
        ["visit", "signup", "purchase"],
        window_end=pd.Timestamp("2026-03-01"),
        maturation_days=14,
    )
    assert res.n_excluded_immature == 20
    assert res.n_entered == 100  # imaturos fora do denominador


def test_runs_on_example_data():
    df = load_example("funnel")
    order = infer_step_order(df)
    res = compute_funnel(df, order)
    assert res.n_entered > 0
    # Conversões devem cair ao longo do funil.
    rates = [s.overall_conversion.rate for s in res.steps]
    assert rates == sorted(rates, reverse=True)
