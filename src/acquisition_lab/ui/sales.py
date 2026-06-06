"""Aba Vendas/Receita — métrica de razão com delta method (bloco 5)."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from ..analysis.ratio import average_order_value, per_user_ticket
from ..viz.sales_viz import (
    plot_bootstrap_distribution,
    plot_ratio_intervals,
    plot_ticket_distribution,
)
from .common import how_to_read, learn_more, missing_data_note
from .i18n import fmt_brl, fmt_int, fmt_num, t


def render(df: pd.DataFrame | None) -> None:
    st.header(t("tab.sales"))
    st.caption(t("sales.caption"))
    how_to_read("sales.help")
    if df is None:
        missing_data_note(t("ds.sales"))
        return

    res = average_order_value(df)
    est = res.estimate

    # 1. Cards de métricas
    c1, c2, c3 = st.columns(3)
    c1.metric(t("sales.metric.aov"), fmt_brl(est.ratio), help=t("sales.metric.aov.help"))
    c1.caption(
        t(
            "common.ci_n_simple",
            lo=fmt_brl(est.lo, markdown=True),
            hi=fmt_brl(est.hi, markdown=True),
            n=fmt_int(est.n_units),
        )
    )
    c2.metric(t("sales.metric.se"), fmt_num(est.se, casas=3), help=t("sales.metric.se.help"))
    c3.metric(
        t("sales.metric.se_naive"),
        fmt_num(est.se_naive, casas=3),
        help=t("sales.metric.se_naive.help"),
    )

    # 2. Comparação das margens
    st.plotly_chart(plot_ratio_intervals(res), use_container_width=True)

    # 3. Toggle do bootstrap
    run_boot = st.checkbox(t("sales.boot_label"), value=False, help=t("sales.boot_help"))

    # 4. Distribuição do ticket por usuário (de onde a média sai)
    tickets = per_user_ticket(df)
    st.plotly_chart(plot_ticket_distribution(tickets, est), use_container_width=True)
    st.caption(t("sales.dist_caption"))

    # 4b. Distribuição do bootstrap, quando ligado
    if run_boot:
        boot_res = average_order_value(df, run_bootstrap=True, n_boot=10000)
        bp, blo, bhi = boot_res.bootstrap
        st.caption(
            t(
                "sales.boot_caption",
                p=fmt_brl(bp, markdown=True),
                lo=fmt_brl(blo, markdown=True),
                hi=fmt_brl(bhi, markdown=True),
            )
        )
        st.plotly_chart(plot_bootstrap_distribution(boot_res), use_container_width=True)
        st.caption(t("sales.boot_dist_caption"))

    # 5. Leitura sobre a covariância, abaixo da distribuição
    if est.cov_xy > 0 and est.se < est.se_naive:
        st.info(t("sales.info_cov_reduces"))
    else:
        st.info(t("sales.info_cov_generic"))

    # 6. Amostra dos dados
    st.subheader(t("sales.sample_subheader"))
    st.dataframe(df.head(20), use_container_width=True, hide_index=True)

    learn_more(["sales.ref.delta", "sales.ref.bootstrap"])
