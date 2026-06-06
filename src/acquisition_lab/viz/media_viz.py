"""Visualização de mídia: série de CAC semanal com change points marcados."""

from __future__ import annotations

import plotly.graph_objects as go

from ..analysis.media import CacResult
from ..ui.i18n import t
from . import theme


def _add_vmarker(fig: go.Figure, x) -> None:
    """Linha vertical pontilhada + rótulo. Usa add_shape/add_annotation em vez de
    add_vline, que falha com x do tipo Timestamp em algumas versões do plotly."""
    fig.add_shape(
        type="line",
        x0=x,
        x1=x,
        yref="paper",
        y0=0,
        y1=1,
        line=dict(color=theme.CHANGE_POINT, width=1.5),
    )
    fig.add_annotation(
        x=x,
        yref="paper",
        y=1.0,
        text=t("viz.changepoint_marker"),
        showarrow=False,
        font=dict(color=theme.CHANGE_POINT, size=10),
        yanchor="bottom",
    )


def plot_cac(result: CacResult) -> go.Figure:
    """Série de CAC semanal (bruta + suavizada) com change points e segmentos.

    O título carrega a defasagem usada. O rótulo de CAC descritivo é
    responsabilidade da camada ``ui`` exibir em destaque ao redor do gráfico.
    """
    weekly = result.weekly
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=weekly["week"],
            y=weekly["cac"],
            mode="lines+markers",
            name=t("viz.media.series_raw"),
            line=dict(color=theme.SERIES_PRIMARY),
            marker=dict(size=4),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=weekly["week"],
            y=weekly["cac_smooth"],
            mode="lines",
            name=t("viz.media.series_smooth"),
            line=dict(color=theme.SERIES_SECONDARY, width=2),
        )
    )

    # Médias por segmento.
    for seg in result.change_points.segments:
        if seg.start >= len(weekly):
            continue
        end = min(seg.end, len(weekly)) - 1
        fig.add_trace(
            go.Scatter(
                x=[weekly["week"].iloc[seg.start], weekly["week"].iloc[end]],
                y=[seg.mean, seg.mean],
                mode="lines",
                line=dict(color=theme.CHANGE_POINT, dash="dash", width=2),
                showlegend=False,
            )
        )

    for week in result.change_point_weeks:
        _add_vmarker(fig, week)

    fig.update_layout(
        title=t("viz.media.title", lag=result.lag_days),
        xaxis_title=t("viz.media.xaxis"),
        yaxis_title=t("viz.media.yaxis"),
        hovermode="x unified",
    )
    return fig
