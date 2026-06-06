"""Aba Visão Geral — números-chave com IC e n, e o rótulo de CAC descritivo."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from ..analysis.cohort import build_retention_matrix
from ..analysis.funnel import compute_funnel, infer_step_order
from ..analysis.media import compute_cac
from ..analysis.ratio import average_order_value
from .common import cac_disclaimer, how_to_read, rate_metric
from .i18n import fmt_brl, fmt_int, fmt_pct, t


def render(data: dict[str, pd.DataFrame | None]) -> None:
    st.header(t("tab.overview"))
    st.caption(t("overview.caption"))
    how_to_read("overview.help")

    loaded = [k for k, v in data.items() if v is not None]
    if not loaded:
        st.info(t("overview.no_data"))
        return

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"**{t('overview.funnel_label')}**")
        if data.get("funnel") is not None:
            df = data["funnel"]
            res = compute_funnel(df, infer_step_order(df))
            rate_metric(t("overview.metric.e2e"), res.end_to_end, t("overview.metric.e2e.help"))
        else:
            st.metric(t("overview.metric.e2e"), "—")

    with col2:
        st.markdown(f"**{t('overview.retention_label')}**")
        matrix = build_retention_matrix(data["cohort"]) if data.get("cohort") is not None else None
        col_p1 = matrix.rates[1].dropna() if matrix is not None else []
        if len(col_p1):
            st.metric(
                t("overview.metric.retention"),
                fmt_pct(float(col_p1.mean())),
                help=t("overview.metric.retention.help"),
            )
            st.caption(t("overview.retention_caption", n=len(col_p1)))
        else:
            st.metric(t("overview.metric.retention"), "—")

    with col3:
        st.markdown(f"**{t('overview.media_label')}**")
        if data.get("media") is not None:
            with st.spinner(t("common.spinner_cac")):
                res = compute_cac(data["media"])
            st.metric(
                t("overview.metric.cac"),
                fmt_brl(res.weekly["cac"].mean()),
                help=t("overview.metric.cac.help"),
            )
            st.caption(t("overview.cac_caption", lag=res.lag_days, n=len(res.change_point_weeks)))
        else:
            st.metric(t("overview.metric.cac"), "—")

    with col4:
        st.markdown(f"**{t('overview.sales_label')}**")
        if data.get("sales") is not None:
            e = average_order_value(data["sales"]).estimate
            st.metric(
                t("overview.metric.aov"),
                fmt_brl(e.ratio),
                help=t("overview.metric.aov.help"),
            )
            st.caption(
                t(
                    "common.ci_n_simple",
                    lo=fmt_brl(e.lo, markdown=True),
                    hi=fmt_brl(e.hi, markdown=True),
                    n=fmt_int(e.n_units),
                )
            )
        else:
            st.metric(t("overview.metric.aov"), "—")

    if data.get("media") is not None:
        st.divider()
        cac_disclaimer()
