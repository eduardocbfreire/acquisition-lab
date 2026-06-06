"""Fonte ÚNICA da paleta e do template Plotly (tons terrosos).

Nenhum outro módulo deve conter hex de cor: todos importam daqui. O template é
registrado em ``plotly.io`` e ativado como default por ``activate()`` (chamado
no ``app.py``).
"""

from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio

TEMPLATE_NAME = "acquisition_lab"

# Paleta categórica (colorway) em tons terrosos.
COLORWAY = ["#B85C38", "#6B705C", "#A98467", "#DDB892", "#582F0E", "#9C6644"]

# Cores de chrome, espelham o .streamlit/config.toml.
PRIMARY = COLORWAY[0]  # cor primária do tema (terracota), igual ao config.toml
BACKGROUND = "#FAF7F2"
SURFACE = "#EFE6DA"
GRID = "#E6DCCD"
TEXT = "#3E2F23"

# Cores semânticas usadas pelos módulos de viz (derivadas da paleta).
SERIES_PRIMARY = COLORWAY[0]  # série principal (terracota)
SERIES_SECONDARY = COLORWAY[2]  # linha suavizada / segunda série
SERIES_TERTIARY = COLORWAY[1]  # barras passo a passo
CHANGE_POINT = COLORWAY[4]  # quebras e médias por segmento (espresso)

# Escala contínua terrosa para o heatmap de coorte (claro -> escuro).
HEATMAP_SCALE = [[0.0, "#FAF7F2"], [1.0, "#582F0E"]]

# Casa com a fonte do corpo da interface (injetada via CSS em ui/common.py).
FONT_FAMILY = "Source Sans 3, Helvetica, Arial, sans-serif"


def _build_template() -> go.layout.Template:
    """Monta o template Plotly com fundo, grid suave, tipografia e margens."""
    axis = dict(
        gridcolor=GRID,
        zerolinecolor=GRID,
        linecolor=GRID,
        ticks="outside",
        tickcolor=GRID,
    )
    layout = go.Layout(
        colorway=COLORWAY,
        paper_bgcolor=BACKGROUND,
        plot_bgcolor=BACKGROUND,
        font=dict(family=FONT_FAMILY, color=TEXT, size=13),
        title=dict(font=dict(color=TEXT, size=17)),
        margin=dict(l=60, r=30, t=70, b=50),
        xaxis=axis,
        yaxis=axis,
        legend=dict(bgcolor=SURFACE, bordercolor=GRID, borderwidth=1),
        colorscale=dict(sequential=HEATMAP_SCALE),
    )
    return go.layout.Template(layout=layout)


def register() -> None:
    """Registra o template em ``plotly.io`` (idempotente)."""
    pio.templates[TEMPLATE_NAME] = _build_template()


def activate() -> None:
    """Registra e define o template terroso como default do Plotly."""
    register()
    pio.templates.default = TEMPLATE_NAME


# Registra no import para que as figuras possam referenciar o template mesmo
# antes de activate() (ex.: testes que não sobem o app).
register()
