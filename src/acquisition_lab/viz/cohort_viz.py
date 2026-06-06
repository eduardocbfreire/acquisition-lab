"""Visualização de coorte: heatmap triangular da matriz de retenção."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from ..analysis.cohort import RetentionMatrix
from ..ui.i18n import t
from . import theme


def plot_retention_heatmap(matrix: RetentionMatrix) -> go.Figure:
    """Heatmap retenção: linhas = coortes, colunas = períodos relativos.

    Células não observadas (matriz triangular) ficam em branco — não imputadas.
    O hover mostra taxa, IC de Wilson 95% e n da coorte.
    """
    rates = matrix.rates
    cohorts = [c.strftime("%Y-%m-%d") for c in rates.index]
    periods = [str(p) for p in rates.columns]
    z = rates.to_numpy(dtype=float)

    customdata = np.dstack(
        [
            matrix.ci_low.to_numpy(dtype=float),
            matrix.ci_high.to_numpy(dtype=float),
            matrix.counts.to_numpy(dtype=float),
            np.repeat(matrix.cohort_sizes.to_numpy(dtype=float)[:, None], z.shape[1], axis=1),
        ]
    )

    text = np.where(
        np.isnan(z), "", np.vectorize(lambda v: f"{v:.0%}" if not np.isnan(v) else "")(z)
    )

    fig = go.Figure(
        go.Heatmap(
            z=z,
            x=periods,
            y=cohorts,
            customdata=customdata,
            colorscale=theme.HEATMAP_SCALE,
            zmin=0,
            zmax=1,
            text=text,
            texttemplate="%{text}",
            textfont=dict(size=10),
            hovertemplate=t("viz.cohort.hover"),
            hoverongaps=False,
        )
    )
    fig.update_layout(
        title=t("viz.cohort.title", gran=t(f"cohort.gran.{matrix.granularity}")),
        xaxis_title=t("viz.cohort.xaxis"),
        yaxis_title=t("viz.cohort.yaxis"),
        yaxis_autorange="reversed",
    )
    return fig
