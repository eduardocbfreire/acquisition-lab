"""Aba Funil."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from ..analysis.funnel import compute_funnel, infer_step_order
from ..viz.funnel_viz import plot_funnel, plot_step_conversions
from .common import how_to_read, missing_data_note, rate_metric
from .i18n import fmt_int, fmt_pct, t


def render(df: pd.DataFrame | None) -> None:
    st.header(t("tab.funnel"))
    st.caption(t("funnel.caption"))
    how_to_read("funnel.help")
    if df is None:
        missing_data_note(t("ds.funnel"))
        return

    inferred = infer_step_order(df)
    col1, col2 = st.columns(2)
    with col1:
        step_order = st.multiselect(
            t("funnel.steps_label"),
            options=inferred,
            default=inferred,
            help=t("funnel.steps_help"),
        )
    with col2:
        maturation = st.slider(
            t("funnel.maturation_label"),
            min_value=0,
            max_value=60,
            value=14,
            help=t("funnel.maturation_help"),
        )
    if len(step_order) < 2:
        st.warning(t("funnel.min_steps_warn"))
        return

    res = compute_funnel(df, step_order, maturation_days=maturation)

    if res.n_entered == 0:
        st.warning(t("err.empty_after_filters"))
        return

    if res.n_excluded_immature > 0:
        st.info(t("funnel.excluded_info", n=fmt_int(res.n_excluded_immature), days=maturation))

    st.plotly_chart(plot_funnel(res), use_container_width=True)
    st.plotly_chart(plot_step_conversions(res), use_container_width=True)

    st.subheader(t("funnel.subheader_e2e"))
    rate_metric(f"{step_order[0]} → {step_order[-1]}", res.end_to_end)
    st.caption(t("funnel.e2e_caption"))

    st.subheader(t("funnel.subheader_detail"))
    rows = []
    for s in res.steps:
        c = s.step_conversion
        rows.append(
            {
                t("funnel.col.step"): s.step,
                t("funnel.col.users"): fmt_int(s.users),
                t("funnel.col.conv_prev"): "—" if c is None else fmt_pct(c.rate),
                t("funnel.col.ci_prev"): "—"
                if c is None
                else f"[{fmt_pct(c.lo)}, {fmt_pct(c.hi)}]",
                t("funnel.col.conv_e2e"): fmt_pct(s.overall_conversion.rate),
            }
        )
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
