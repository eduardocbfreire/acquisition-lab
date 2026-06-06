"""Visualização de vendas: comparação de IC do ticket médio (razão)."""

from __future__ import annotations

import plotly.graph_objects as go

from ..analysis.ratio import AovResult
from ..ui.i18n import fmt_brl, t
from . import theme


def plot_ratio_intervals(result: AovResult) -> go.Figure:
    """Compara o IC do delta method, do ingênuo (denominador constante) e,
    se houver, do bootstrap — todos sobre o mesmo ponto de razão."""
    est = result.estimate
    methods, points, los, his = [], [], [], []

    methods.append(t("viz.sales.method.delta"))
    points.append(est.ratio)
    los.append(est.ratio - est.lo)
    his.append(est.hi - est.ratio)

    methods.append(t("viz.sales.method.naive"))
    points.append(est.ratio)
    los.append(1.96 * est.se_naive)
    his.append(1.96 * est.se_naive)

    if result.bootstrap is not None:
        bp, blo, bhi = result.bootstrap
        methods.append(t("viz.sales.method.boot"))
        points.append(bp)
        los.append(bp - blo)
        his.append(bhi - bp)

    fig = go.Figure(
        go.Scatter(
            x=methods,
            y=points,
            mode="markers",
            marker=dict(size=12, color=theme.SERIES_PRIMARY),
            error_y=dict(type="data", symmetric=False, array=his, arrayminus=los),
        )
    )
    fig.update_layout(
        title=t("viz.sales.title", ratio=fmt_brl(est.ratio)),
        yaxis_title=t("viz.sales.yaxis"),
    )
    return fig
