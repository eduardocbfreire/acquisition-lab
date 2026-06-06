"""Aba Mídia."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from ..analysis.changepoints import MIN_SERIES_LENGTH
from ..analysis.media import compute_cac, estimate_lag
from ..viz.media_viz import plot_cac
from .common import cac_disclaimer, how_to_read, missing_data_note
from .i18n import fmt_brl, t


def render(df: pd.DataFrame | None) -> None:
    st.header(t("tab.media"))
    st.caption(t("media.caption"))
    how_to_read("media.help")
    # Rótulo obrigatório, exibido ANTES de qualquer número de CAC.
    cac_disclaimer()

    if df is None:
        missing_data_note(t("ds.media"))
        return

    auto_lag = estimate_lag(df["spend"].to_numpy(float), df["conversions"].to_numpy(float))
    col1, col2 = st.columns(2)
    with col1:
        use_auto = st.checkbox(t("media.auto_lag_label", lag=auto_lag), value=True)
    with col2:
        manual_lag = st.slider(t("media.manual_lag_label"), 0, 30, auto_lag, disabled=use_auto)
    smooth = st.slider(t("media.smooth_label"), 1, 8, 4)

    lag = None if use_auto else manual_lag
    with st.spinner(t("common.spinner_cac")):
        res = compute_cac(df, lag_days=lag, smooth_weeks=smooth, min_size=4)

    m1, m2, m3 = st.columns(3)
    m1.metric(
        t("media.metric.lag"),
        t("media.metric.lag.value", lag=res.lag_days),
        help=t("media.metric.lag.help"),
    )
    m2.metric(
        t("media.metric.cac"), fmt_brl(res.weekly["cac"].mean()), help=t("media.metric.cac.help")
    )
    m3.metric(
        t("media.metric.cps"), f"{len(res.change_point_weeks)}", help=t("media.metric.cps.help")
    )

    st.plotly_chart(plot_cac(res), use_container_width=True)

    if res.change_point_weeks:
        st.write(f"**{t('media.cps_found')}**")
        st.write(", ".join(w.strftime("%Y-%m-%d") for w in res.change_point_weeks))
    elif not res.change_points.enabled:
        st.info(t("cp.min_points", min=MIN_SERIES_LENGTH, n=res.change_points.n))

    cac_disclaimer()  # repetido após o gráfico: o rótulo acompanha todo CAC
