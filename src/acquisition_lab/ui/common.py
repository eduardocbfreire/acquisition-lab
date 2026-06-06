"""Helpers de UI reaproveitados pelas abas (incluindo o CSS, em um só lugar)."""

from __future__ import annotations

import streamlit as st

from ..analysis.stats import ProportionEstimate
from ..viz import theme
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

# Estiliza o radio de navegação (key="nav") como abas: itens lado a lado, sem a
# bolinha do radio, item ativo com borda inferior na cor primária. Cores vêm do
# theme.py (fonte única); escopo em .st-key-nav para não afetar o radio de idioma.
_NAV_CSS = f"""
<style>
.st-key-nav [role="radiogroup"] {{
    flex-direction: row;
    flex-wrap: wrap;
    gap: 0.25rem;
    border-bottom: 2px solid {theme.GRID};
    margin-bottom: 1rem;
}}
.st-key-nav [role="radiogroup"] > label {{
    padding: 0.4rem 1rem;
    margin: 0 0 -2px 0;
    border-bottom: 2px solid transparent;
    cursor: pointer;
}}
.st-key-nav [role="radiogroup"] > label > div:first-child {{
    display: none;
}}
.st-key-nav [role="radiogroup"] > label:has(input:checked) {{
    border-bottom-color: {theme.PRIMARY};
    font-weight: 600;
}}
</style>
"""


def _uploader_css() -> str:
    """Traduz os textos embutidos do uploader do Streamlit ('Drag and drop...',
    'Browse files', 'Limit...') via CSS. O original é colapsado com font-size:0 e
    o texto do i18n entra por ::before/::after — o ícone do dropzone fica intacto."""
    return f"""
<style>
[data-testid="stFileUploaderDropzoneInstructions"] > div:last-child {{ font-size: 0; }}
[data-testid="stFileUploaderDropzoneInstructions"] > div:last-child::before {{
    content: "{t("uploader.drag")}";
    font-size: 0.9rem;
    display: block;
}}
[data-testid="stFileUploaderDropzoneInstructions"] > div:last-child::after {{
    content: "{t("uploader.limit")}";
    font-size: 0.78rem;
    display: block;
    opacity: 0.6;
}}
[data-testid="stFileUploaderDropzone"] button {{ font-size: 0; }}
[data-testid="stFileUploaderDropzone"] button::before {{
    content: "{t("uploader.browse")}";
    font-size: 0.875rem;
}}
</style>
"""


def inject_css() -> None:
    """Injeta o CSS do projeto. Chamar uma vez, depois de definido o idioma.

    Precisa rodar com o idioma já escolhido (após ``set_lang``), porque o override
    do uploader usa ``t()`` para traduzir os textos embutidos do Streamlit.
    """
    st.markdown(_CSS, unsafe_allow_html=True)
    st.markdown(_NAV_CSS, unsafe_allow_html=True)
    st.markdown(_uploader_css(), unsafe_allow_html=True)


def how_to_read(body_key: str) -> None:
    """Expander 'Como ler esta tela?' no topo da aba, fechado por padrão."""
    with st.expander(t("common.how_to_read"), expanded=False):
        st.markdown(t(body_key))


def learn_more(ref_keys: list[str]) -> None:
    """Expander 'Para entender mais' ao fim da aba, com referências comentadas."""
    with st.expander(t("common.learn_more"), expanded=False):
        for key in ref_keys:
            st.markdown(f"- {t(key)}")


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
