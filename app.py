"""acquisition-lab — app Streamlit.

Roda localmente e offline. Sobe CSVs de funil, coorte, mídia e vendas (ou usa
os exemplos sintéticos inclusos) e devolve análises de aquisição com detecção
de change points. Este arquivo só monta a interface: a lógica vive em
``acquisition_lab.analysis`` (puro) e ``acquisition_lab.viz``.

    streamlit run app.py
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from acquisition_lab.ingest import SCHEMAS, CsvValidationError, load_csv, load_example
from acquisition_lab.ui import changepoints, cohort, funnel, media, overview, sales
from acquisition_lab.ui.common import inject_css
from acquisition_lab.ui.i18n import fmt_int, set_lang, t
from acquisition_lab.viz import theme

st.set_page_config(page_title="Acquisition Lab", layout="wide")
theme.activate()  # template Plotly terroso como default em todos os gráficos


_LANG_BY_CHOICE = {"PT": "pt", "EN": "en"}
_CHOICE_BY_LANG = {"pt": "PT", "en": "EN"}


def _on_lang_change() -> None:
    """Copia a escolha do widget para o idioma persistente."""
    st.session_state["lang"] = _LANG_BY_CHOICE[st.session_state["lang_choice"]]


def _select_language() -> None:
    """Toggle PT/EN no topo da barra lateral; define o idioma desta execução.

    O rótulo é estático de propósito: se viesse de ``t()``, mudaria de idioma a
    cada clique e o Streamlit trataria como um widget novo, perdendo a seleção. O
    idioma fica em ``session_state['lang']``, separado da key do widget, e o
    ``index`` é recalculado a partir dele a cada execução.
    """
    if "lang" not in st.session_state:
        st.session_state["lang"] = "pt"
    index = ["PT", "EN"].index(_CHOICE_BY_LANG[st.session_state["lang"]])
    st.sidebar.radio(
        "Language · Idioma",
        ["PT", "EN"],
        index=index,
        horizontal=True,
        key="lang_choice",
        on_change=_on_lang_change,
    )
    set_lang(st.session_state["lang"])


def _load_dataset(key: str) -> pd.DataFrame | None:
    """Widget de upload/exemplo por dataset, com tratamento de erro de formato."""
    schema = SCHEMAS[key]
    name = t(f"ds.{key}")
    with st.sidebar.expander(name, expanded=False):
        use_example = st.checkbox(t("sidebar.use_example"), value=True, key=f"ex_{key}")
        upload = st.file_uploader(
            t("sidebar.upload_label", name=name),
            type=["csv"],
            key=f"up_{key}",
            help=t("sidebar.upload_help", header=schema.header_example),
        )
        st.caption(f"`{schema.header_example}`")

        source, origin = None, None
        if upload is not None:
            source, origin = upload, "upload"
        elif use_example:
            origin = "exemplo"

        try:
            if origin == "upload":
                df = load_csv(source.getvalue(), key)
                st.success(t("sidebar.rows_upload", n=fmt_int(len(df))))
                return df
            if origin == "exemplo":
                df = load_example(key)
                st.success(t("sidebar.rows_example", n=fmt_int(len(df))))
                return df
        except CsvValidationError as exc:
            st.error(t("sidebar.err_csv", name=name, detail=exc))
            return None
        except Exception as exc:  # rede de segurança no ponto de entrada
            st.error(t("sidebar.err_unexpected", name=name, detail=exc))
            return None
    return None


def main() -> None:
    inject_css()
    _select_language()

    st.title(t("app.title"))
    st.caption(t("app.caption"))

    st.sidebar.title(t("sidebar.data_title"))
    st.sidebar.caption(t("sidebar.data_caption"))
    data = {key: _load_dataset(key) for key in ("funnel", "cohort", "media", "sales")}

    tabs = st.tabs(
        [
            t("tab.overview"),
            t("tab.funnel"),
            t("tab.cohort"),
            t("tab.media"),
            t("tab.changepoints"),
            t("tab.sales"),
        ]
    )
    renderers = (
        lambda: overview.render(data),
        lambda: funnel.render(data["funnel"]),
        lambda: cohort.render(data["cohort"]),
        lambda: media.render(data["media"]),
        lambda: changepoints.render(data),
        lambda: sales.render(data["sales"]),
    )
    for tab, render in zip(tabs, renderers):
        with tab:
            render()


if __name__ == "__main__":
    main()
