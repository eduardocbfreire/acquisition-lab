"""Visualização de vendas: comparação de métodos e distribuições do ticket."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from ..analysis.ratio import AovResult
from ..analysis.stats import RatioEstimate
from ..ui.i18n import fmt_brl, t
from . import theme


def plot_ratio_intervals(result: AovResult) -> go.Figure:
    """Barras de erro HORIZONTAIS: delta method × ingênua, sobre o mesmo ponto.

    Eixo y com os dois métodos, eixo x com o ticket em R$. O eixo x não começa
    em zero — usa folga justa em volta dos intervalos para a diferença de largura
    ficar legível. Ticket e largura da margem vão no hover, com moeda central.
    """
    est = result.estimate
    delta_half = est.hi - est.ratio  # 1.96 * se (delta method)
    naive_half = 1.96 * est.se_naive

    methods = [t("viz.sales.method.delta"), t("viz.sales.method.naive")]
    halves = [delta_half, naive_half]
    hover = [
        t("viz.sales.compare_hover", ratio=fmt_brl(est.ratio), half=fmt_brl(h)) for h in halves
    ]

    fig = go.Figure(
        go.Scatter(
            x=[est.ratio, est.ratio],
            y=methods,
            mode="markers",
            marker=dict(size=11, color=theme.SERIES_PRIMARY),
            error_x=dict(
                type="data",
                array=halves,
                arrayminus=halves,
                thickness=2,
                width=8,
                color=theme.SERIES_PRIMARY,
            ),
            hovertext=hover,
            hovertemplate="%{hovertext}<extra></extra>",
        )
    )
    lo = est.ratio - max(halves)
    hi = est.ratio + max(halves)
    pad = (hi - lo) * 0.35 or 1.0
    fig.update_layout(
        title=t("viz.sales.title", ratio=fmt_brl(est.ratio)),
        xaxis_title=t("viz.sales.compare_xaxis"),
        xaxis=dict(range=[lo - pad, hi + pad]),
        yaxis=dict(autorange="reversed"),  # delta method no topo
        height=220,
        margin=dict(l=10, r=10, t=50, b=40),
    )
    return fig


def plot_ticket_distribution(tickets: np.ndarray, est: RatioEstimate) -> go.Figure:
    """Histograma do ticket por usuário, com a média (AOV) e a faixa do IC 95%."""
    fig = go.Figure(go.Histogram(x=tickets, nbinsx=50, marker_color=theme.SERIES_PRIMARY))
    fig.add_vrect(x0=est.lo, x1=est.hi, fillcolor=theme.CHANGE_POINT, opacity=0.15, line_width=0)
    fig.add_vline(
        x=est.ratio,
        line=dict(color=theme.CHANGE_POINT, width=2),
        annotation_text=t("viz.sales.dist.aov_line"),
        annotation_position="top",
    )
    fig.update_layout(
        title=t("viz.sales.dist.title"),
        xaxis_title=t("viz.sales.dist.xaxis"),
        yaxis_title=t("viz.sales.dist.yaxis"),
        bargap=0.03,
    )
    return fig


def plot_bootstrap_distribution(result: AovResult) -> go.Figure:
    """Histograma das estimativas reamostradas: faixa do IC percentil (bootstrap)
    sombreada e o IC do delta method em duas linhas, para comparar os métodos."""
    samples = result.bootstrap_samples
    _, boot_lo, boot_hi = result.bootstrap
    est = result.estimate

    fig = go.Figure(go.Histogram(x=samples, nbinsx=50, marker_color=theme.SERIES_TERTIARY))
    fig.add_vrect(
        x0=boot_lo,
        x1=boot_hi,
        fillcolor=theme.SERIES_PRIMARY,
        opacity=0.18,
        line_width=0,
        annotation_text=t("viz.sales.boot.band"),
        annotation_position="top left",
    )
    for x in (est.lo, est.hi):
        fig.add_vline(x=x, line=dict(color=theme.CHANGE_POINT, width=2, dash="dash"))
    fig.add_annotation(
        x=est.hi,
        yref="paper",
        y=1.0,
        text=t("viz.sales.boot.delta"),
        showarrow=False,
        font=dict(color=theme.CHANGE_POINT, size=11),
        yanchor="bottom",
    )
    fig.update_layout(
        title=t("viz.sales.boot.title"),
        xaxis_title=t("viz.sales.boot.xaxis"),
        yaxis_title=t("viz.sales.boot.yaxis"),
        bargap=0.03,
    )
    return fig
