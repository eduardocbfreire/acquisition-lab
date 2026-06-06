"""Visualização de change points: série com quebras e médias por segmento."""

from __future__ import annotations

from typing import Sequence

import plotly.graph_objects as go

from ..analysis.changepoints import ChangePointResult
from ..ui.i18n import t
from . import theme


def plot_change_points(
    x: Sequence,
    y: Sequence,
    result: ChangePointResult,
    *,
    title: str = "",
    y_label: str = "",
) -> go.Figure:
    """Plota a série, as linhas verticais dos change points e as médias por segmento."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(x),
            y=list(y),
            mode="lines+markers",
            name=y_label,
            line=dict(color=theme.SERIES_PRIMARY),
            marker=dict(size=4),
        )
    )

    # Médias por segmento (degraus).
    for seg in result.segments:
        if seg.start >= len(x):
            continue
        end = min(seg.end, len(x)) - 1
        fig.add_trace(
            go.Scatter(
                x=[x[seg.start], x[end]],
                y=[seg.mean, seg.mean],
                mode="lines",
                line=dict(color=theme.CHANGE_POINT, dash="dash", width=2),
                name=t("viz.cp.segment_mean", mean=f"{seg.mean:.2f}"),
                showlegend=False,
            )
        )

    # Linhas verticais nos change points (add_shape aceita x do tipo Timestamp).
    for idx in result.indices:
        if idx < len(x):
            fig.add_shape(
                type="line",
                x0=x[idx],
                x1=x[idx],
                yref="paper",
                y0=0,
                y1=1,
                line=dict(color=theme.CHANGE_POINT, width=1.5),
            )
            fig.add_annotation(
                x=x[idx],
                yref="paper",
                y=1.0,
                text=t("viz.changepoint_marker"),
                showarrow=False,
                font=dict(color=theme.CHANGE_POINT, size=10),
                yanchor="bottom",
            )

    if result.enabled:
        subtitle = t(
            "viz.cp.subtitle",
            model=result.model,
            pen=f"{result.penalty:.2f}",
            sigma=f"{result.sigma2:.3g}",
            min=result.min_size,
        )
    else:
        subtitle = t("viz.cp.disabled", message=result.message)

    fig.update_layout(
        title=f"{title}<br><sub>{subtitle}</sub>",
        xaxis_title=t("viz.cp.xaxis"),
        yaxis_title=y_label,
        hovermode="x unified",
    )
    return fig
