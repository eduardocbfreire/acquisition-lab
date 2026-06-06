"""Visualização de funil: barras por etapa com IC de Wilson e n absoluto."""

from __future__ import annotations

import plotly.graph_objects as go

from ..analysis.funnel import FunnelResult
from ..ui.i18n import fmt_int, fmt_pct, t
from . import theme


def plot_funnel(result: FunnelResult) -> go.Figure:
    """Barras de usuários por etapa, anotadas com conversão passo a passo e n."""
    steps = result.steps
    labels = [s.step for s in steps]
    users = [s.users for s in steps]

    text = []
    for s in steps:
        line_n = t("viz.funnel.n", n=fmt_int(s.users))
        if s.step_conversion is None:
            text.append(line_n)
        else:
            c = s.step_conversion
            conv = t("viz.funnel.conv_prev", rate=fmt_pct(c.rate))
            ci = t("viz.funnel.ci", lo=fmt_pct(c.lo), hi=fmt_pct(c.hi))
            text.append(f"{line_n}<br>{conv}<br>{ci}")

    fig = go.Figure(
        go.Funnel(
            y=labels,
            x=users,
            text=text,
            textposition="inside",
            textinfo="text",
            marker=dict(color=theme.SERIES_PRIMARY),
        )
    )
    fig.update_layout(
        title=t(
            "viz.funnel.title",
            entered=fmt_int(result.n_entered),
            excluded=fmt_int(result.n_excluded_immature),
        ),
    )
    return fig


def plot_step_conversions(result: FunnelResult) -> go.Figure:
    """Barras de conversão passo a passo com barras de erro do IC de Wilson."""
    steps = [s for s in result.steps if s.step_conversion is not None]
    labels = [
        f"{result.steps[i].step}→{result.steps[i + 1].step}" for i in range(len(result.steps) - 1)
    ]
    rates = [s.step_conversion.rate for s in steps]
    los = [s.step_conversion.rate - s.step_conversion.lo for s in steps]
    his = [s.step_conversion.hi - s.step_conversion.rate for s in steps]
    ns = [s.step_conversion.nobs for s in steps]

    fig = go.Figure(
        go.Bar(
            x=labels,
            y=rates,
            error_y=dict(type="data", symmetric=False, array=his, arrayminus=los),
            marker=dict(color=theme.SERIES_TERTIARY),
            text=[f"{fmt_pct(r)}<br>{t('viz.funnel.n', n=fmt_int(n))}" for r, n in zip(rates, ns)],
            textposition="outside",
        )
    )
    fig.update_layout(
        title=t("viz.funnel.step_title"),
        yaxis_title=t("viz.funnel.step_yaxis"),
        yaxis_tickformat=".0%",
    )
    return fig
