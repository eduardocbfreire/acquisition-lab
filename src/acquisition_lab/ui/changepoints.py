"""Aba Change Points — detecção interativa sobre séries derivadas dos dados."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from ..analysis.changepoints import MIN_SERIES_LENGTH, detect_change_points
from ..analysis.media import compute_cac
from ..viz.changepoints_viz import plot_change_points
from .common import how_to_read, learn_more
from .i18n import fmt_int, t

COST_OPTIONS = ["l2", "normal", "linear"]


def _build_series(data: dict[str, pd.DataFrame | None]) -> dict[str, tuple]:
    """Séries candidatas por id -> (x, y, sugestão de min_size). O rótulo visível
    vem do i18n (``cp.series.<id>``), então nada de texto fixo aqui."""
    series: dict[str, tuple] = {}

    media = data.get("media")
    if media is not None:
        m = media.sort_values("date")
        series["spend"] = (m["date"], m["spend"], 7)
        series["conv"] = (m["date"], m["conversions"], 7)
        cac = compute_cac(media, min_size=4, detect=False)
        series["cac"] = (cac.weekly["week"], cac.weekly["cac"], 4)

    cohort = data.get("cohort")
    if cohort is not None:
        daily = (
            cohort.assign(signup_date=pd.to_datetime(cohort["signup_date"]))
            .drop_duplicates("user_id")
            .groupby("signup_date")["user_id"]
            .count()
            .sort_index()
        )
        series["signups"] = (daily.index, daily.values, 7)

    return series


def render(data: dict[str, pd.DataFrame | None]) -> None:
    st.header(t("tab.changepoints"))
    st.caption(t("cp.caption"))
    how_to_read("cp.help")

    series = _build_series(data)
    if not series:
        st.info(t("cp.no_data"))
        return

    series_id = st.selectbox(
        t("cp.series_label"), options=list(series), format_func=lambda s: t(f"cp.series.{s}")
    )
    x, y, suggested_min = series[series_id]
    label = t(f"cp.series.{series_id}")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        model = st.selectbox(
            t("cp.cost_label"),
            options=COST_OPTIONS,
            index=0,
            format_func=lambda c: t(f"cp.cost.{c}"),
            help=t("cp.cost_help"),
        )
    with c2:
        k = st.slider(t("cp.k_label"), 0.5, 3.0, 1.0, 0.1, help=t("cp.k_help"))
    with c3:
        min_size = st.slider(
            t("cp.minsize_label"), 2, 20, int(suggested_min), help=t("cp.minsize_help")
        )
    with c4:
        detrend = st.checkbox(t("cp.detrend_label"), value=False, help=t("cp.detrend_help"))

    with st.spinner(t("cp.spinner")):
        res = detect_change_points(list(y), model=model, k=k, min_size=min_size, detrend=detrend)

    if not res.enabled:
        st.warning(t("cp.min_points", min=MIN_SERIES_LENGTH, n=res.n))
        return

    st.plotly_chart(
        plot_change_points(list(x), list(y), res, title=label, y_label=label),
        use_container_width=True,
    )

    c1, c2, c3 = st.columns(3)
    c1.metric(t("cp.metric.cps"), len(res.indices))
    c2.metric(t("cp.metric.sigma"), f"{res.sigma2:.3g}", help=t("cp.metric.sigma.help"))
    c3.metric(t("cp.metric.pen"), f"{res.penalty:.2f}", help=t("cp.metric.pen.help"))

    if res.dropped_low_magnitude:
        st.caption(t("cp.dropped_mag", n=fmt_int(len(res.dropped_low_magnitude))))
    if res.dropped_unstable:
        st.caption(t("cp.dropped_unstable", n=fmt_int(len(res.dropped_unstable))))

    learn_more(["cp.ref.ruptures", "cp.ref.truong", "cp.ref.killick"])
