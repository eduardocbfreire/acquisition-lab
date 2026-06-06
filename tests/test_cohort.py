"""Bloco 3 — coorte / retenção."""

import numpy as np

from acquisition_lab.analysis.cohort import build_retention_matrix
from acquisition_lab.ingest import load_example


def test_period_zero_is_full_and_matrix_is_triangular():
    df = load_example("cohort")
    m = build_retention_matrix(df, granularity="W", max_period=12)
    # Período 0: todos ativos no signup por construção -> retenção 1.0.
    assert np.allclose(m.rates[0].dropna().to_numpy(), 1.0)
    # Triangular: coorte mais recente tem menos períodos observados que a mais antiga.
    observed_per_cohort = m.rates.notna().sum(axis=1)
    assert observed_per_cohort.iloc[-1] < observed_per_cohort.iloc[0]


def test_no_imputation_unobserved_cells_are_nan():
    df = load_example("cohort")
    m = build_retention_matrix(df, granularity="W", max_period=12)
    # A coorte mais recente não tem 12 períodos maduros -> células finais NaN.
    last = m.rates.iloc[-1]
    assert last.isna().any()


def test_cell_has_count_and_ci():
    df = load_example("cohort")
    m = build_retention_matrix(df, granularity="W", max_period=12)
    cohort0 = m.rates.index[0]
    rate = m.rates.loc[cohort0, 1]
    lo = m.ci_low.loc[cohort0, 1]
    hi = m.ci_high.loc[cohort0, 1]
    assert lo <= rate <= hi
    assert m.counts.loc[cohort0, 1] >= 0
    assert m.cohort_sizes.loc[cohort0] > 0


def test_retention_decays_over_periods():
    df = load_example("cohort")
    m = build_retention_matrix(df, granularity="W", max_period=12)
    first_cohort = m.rates.iloc[0].dropna()
    # Retenção em t=1 maior que em t=6 (decaimento).
    assert first_cohort[1] > first_cohort[6]
