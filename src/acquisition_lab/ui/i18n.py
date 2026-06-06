"""Internacionalização e formatação de números dependente de idioma.

Fonte única das strings visíveis (PT/EN) e dos formatadores de número, que
também variam com o idioma (PT usa 1.234,56; EN usa 1,234.56). Não importa
``streamlit`` — o idioma atual fica num estado de módulo, definido por
``set_lang`` a cada execução do app —, então os módulos de ``viz`` podem chamar
``t()`` e os formatadores sem deixar de ser puros.
"""

from __future__ import annotations

import math

from .i18n_en import EN
from .i18n_pt import PT

STRINGS: dict[str, dict[str, str]] = {"pt": PT, "en": EN}
LANGUAGES = ("pt", "en")
DEFAULT_LANG = "pt"

# Garante paridade de chaves: nada de string traduzida pela metade.
_missing = set(PT) ^ set(EN)
if _missing:
    raise RuntimeError(f"chaves de i18n sem par PT/EN: {sorted(_missing)}")

_state = {"lang": DEFAULT_LANG}


def set_lang(lang: str) -> None:
    """Define o idioma atual (chamado uma vez por execução, no app.py)."""
    _state["lang"] = lang if lang in STRINGS else DEFAULT_LANG


def get_lang() -> str:
    """Idioma atual ('pt' ou 'en')."""
    return _state["lang"]


def t(key: str, **kwargs: object) -> str:
    """Texto da chave no idioma atual, com interpolação opcional via ``str.format``.

    Sem ``kwargs``, devolve a string crua (preserva ``%{...}`` de hovertemplates
    do Plotly). Chave ausente cai para o texto em PT e, por fim, para a própria
    chave, para nunca quebrar a interface.
    """
    lang = _state["lang"]
    text = STRINGS[lang].get(key) or STRINGS[DEFAULT_LANG].get(key) or key
    return text.format(**kwargs) if kwargs else text


# --------------------------------------------------------------------------- #
# Formatação de números — varia com o idioma.
# --------------------------------------------------------------------------- #
def _is_nan(value: float) -> bool:
    return value is None or (isinstance(value, float) and math.isnan(value))


def fmt_pct(value: float, casas: int = 1) -> str:
    """Percentual (PT '8,5%'; EN '8.5%'). Vazio vira travessão."""
    if _is_nan(value):
        return "—"
    text = f"{value * 100:.{casas}f}"
    return (text.replace(".", ",") if get_lang() == "pt" else text) + "%"


def fmt_int(value: float) -> str:
    """Inteiro com separador de milhar (PT '1.234'; EN '1,234')."""
    if _is_nan(value):
        return "—"
    grouped = f"{int(round(value)):,}"
    return grouped.replace(",", ".") if get_lang() == "pt" else grouped


def fmt_brl(value: float, casas: int = 2) -> str:
    """Reais (PT 'R$ 1.234,56'; EN 'R$ 1,234.56'). A moeda é sempre real."""
    if _is_nan(value):
        return "—"
    base = f"{value:,.{casas}f}"
    if get_lang() == "pt":
        base = base.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {base}"
