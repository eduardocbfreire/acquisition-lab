"""Helpers de UI reaproveitados pelas abas (incluindo o CSS, em um só lugar)."""

from __future__ import annotations

import streamlit as st

from ..analysis.stats import ProportionEstimate
from .i18n import fmt_int, fmt_pct, t

# CSS único do projeto: fontes do Google (Fraunces nos títulos, Source Sans 3 no
# corpo) e esconde o menu/toolbar para travar o tema. Injetado uma vez no app.py.
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Source+Sans+3:wght@400;600&display=swap');
html, body, [class*="css"], [data-testid="stMarkdownContainer"] {
    font-family: 'Source Sans 3', sans-serif;
}
h1, h2, h3, [data-testid="stHeading"] {
    font-family: 'Fraunces', Georgia, serif;
    letter-spacing: -0.01em;
}
#MainMenu { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
footer { visibility: hidden; }
</style>
"""


def inject_css() -> None:
    """Injeta o CSS do projeto. Chamar uma única vez, no início do app."""
    st.markdown(_CSS, unsafe_allow_html=True)


def how_to_read(body_key: str) -> None:
    """Expander 'Como ler esta tela?' no topo da aba, fechado por padrão."""
    with st.expander(t("common.how_to_read"), expanded=False):
        st.markdown(t(body_key))


def rate_metric(label: str, est: ProportionEstimate, help_text: str | None = None) -> None:
    """Taxa com IC de Wilson e o n absoluto ao lado (princípio da spec)."""
    if est is None or est.nobs == 0:
        st.metric(label, "—")
        return
    st.metric(label, fmt_pct(est.rate), help=help_text)
    st.caption(
        t(
            "common.ci_n",
            lo=fmt_pct(est.lo),
            hi=fmt_pct(est.hi),
            n=fmt_int(est.nobs),
            count=fmt_int(est.count),
            total=fmt_int(est.nobs),
        )
    )


def cac_disclaimer() -> None:
    """Rótulo visível, obrigatório em todo lugar que mostra CAC. Não suavizar."""
    st.warning(t("common.cac_disclaimer"))


def missing_data_note(dataset_name: str) -> None:
    """Aviso de aba sem dados, com o nome do conjunto já traduzido."""
    st.info(t("common.missing_data", name=dataset_name))
