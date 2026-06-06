"""Aba Coorte."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from ..analysis.cohort import build_retention_matrix
from ..viz.cohort_viz import plot_retention_heatmap
from .common import how_to_read, missing_data_note
from .i18n import t


def render(df: pd.DataFrame | None) -> None:
    st.header(t("tab.cohort"))
    st.caption(t("cohort.caption"))
    how_to_read("cohort.help")
    if df is None:
        missing_data_note(t("ds.cohort"))
        return

    col1, col2 = st.columns(2)
    with col1:
        gran = st.selectbox(
            t("cohort.gran_label"),
            options=["W", "M"],
            index=0,
            format_func=lambda g: t(f"cohort.gran.{g}"),
        )
    with col2:
        max_period = st.slider(t("cohort.periods_label"), min_value=4, max_value=24, value=12)

    matrix = build_retention_matrix(df, granularity=gran, max_period=max_period)

    st.plotly_chart(plot_retention_heatmap(matrix), use_container_width=True)
    st.warning(t("cohort.warn"))

    st.subheader(t("cohort.sizes_subheader"))
    sizes = matrix.cohort_sizes.reset_index()
    sizes.columns = [t("cohort.col.cohort"), t("cohort.col.size")]
    sizes[t("cohort.col.cohort")] = sizes[t("cohort.col.cohort")].dt.strftime("%Y-%m-%d")
    st.dataframe(sizes, use_container_width=True, hide_index=True)
