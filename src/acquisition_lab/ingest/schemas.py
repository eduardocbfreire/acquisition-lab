"""Definição das colunas esperadas por CSV — fonte única de verdade.

Cada ``DatasetSchema`` lista as colunas obrigatórias, seu tipo lógico
(``datetime``, ``numeric``, ``str``) e um exemplo de linha. Os loaders usam
isso para validar uploads e gerar mensagens de erro claras.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Column:
    name: str
    kind: str  # "datetime" | "numeric" | "str"
    description: str


@dataclass(frozen=True)
class DatasetSchema:
    key: str
    title: str
    columns: tuple[Column, ...]
    example_file: str
    header_example: str
    row_example: str

    @property
    def required_names(self) -> list[str]:
        return [c.name for c in self.columns]


SCHEMAS: dict[str, DatasetSchema] = {
    "funnel": DatasetSchema(
        key="funnel",
        title="Funil",
        columns=(
            Column("user_id", "str", "identificador único do usuário"),
            Column("step", "str", "nome da etapa do funil"),
            Column("event_time", "datetime", "timestamp do evento na etapa"),
        ),
        example_file="funnel.csv",
        header_example="user_id,step,event_time",
        row_example="u000001,signup,2026-01-15 09:32:10",
    ),
    "cohort": DatasetSchema(
        key="cohort",
        title="Coorte",
        columns=(
            Column("user_id", "str", "identificador único do usuário"),
            Column("signup_date", "datetime", "data de aquisição (define a coorte)"),
            Column("activity_date", "datetime", "data do evento qualificador de retenção"),
        ),
        example_file="cohort.csv",
        header_example="user_id,signup_date,activity_date",
        row_example="c000001,2026-01-12,2026-02-09",
    ),
    "media": DatasetSchema(
        key="media",
        title="Mídia",
        columns=(
            Column("date", "datetime", "dia"),
            Column("spend", "numeric", "gasto de mídia no dia"),
            Column("conversions", "numeric", "aquisições atribuídas no dia"),
        ),
        example_file="media_spend.csv",
        header_example="date,spend,conversions",
        row_example="2026-01-15,2243.10,52",
    ),
    "sales": DatasetSchema(
        key="sales",
        title="Vendas",
        columns=(
            Column("user_id", "str", "identificador único do usuário"),
            Column("revenue", "numeric", "receita total do usuário"),
            Column("orders", "numeric", "número de pedidos do usuário"),
        ),
        example_file="sales.csv",
        header_example="user_id,revenue,orders",
        row_example="s000001,165.56,2",
    ),
}
