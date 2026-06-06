"""Leitura e validação de CSVs com mensagens de erro claras.

Ponto de entrada de dados: tudo que chega de upload passa por ``load_csv``,
que valida contra o ``DatasetSchema`` e converte os tipos. Erros de formato
viram ``CsvValidationError`` com mensagem acionável, em vez de stack trace.
"""

from __future__ import annotations

import os
from io import BytesIO, StringIO
from typing import IO

import pandas as pd

from .schemas import SCHEMAS, DatasetSchema

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
    "data",
)


class CsvValidationError(ValueError):
    """Erro de formato de CSV, com mensagem voltada ao usuário.

    ``code``/``params`` permitem que a camada de UI traduza a mensagem via i18n
    (o ``ingest`` é puro e não conhece idioma). A mensagem em texto é o fallback.
    """

    def __init__(self, message: str, *, code: str | None = None, params: dict | None = None):
        super().__init__(message)
        self.code = code
        self.params = params or {}


def _read_raw(source: str | IO[bytes] | IO[str]) -> pd.DataFrame:
    try:
        return pd.read_csv(source)
    except pd.errors.EmptyDataError as exc:
        raise CsvValidationError("o arquivo está vazio.") from exc
    except pd.errors.ParserError as exc:
        raise CsvValidationError(f"não consegui parsear o CSV (formato inválido): {exc}") from exc
    except UnicodeDecodeError as exc:
        raise CsvValidationError("o arquivo não está em UTF-8. Reexporte o CSV em UTF-8.") from exc


def _coerce_and_validate(df: pd.DataFrame, schema: DatasetSchema) -> pd.DataFrame:
    # Normaliza nomes de colunas (espaços extras).
    df = df.rename(columns={c: str(c).strip() for c in df.columns})

    missing = [c for c in schema.required_names if c not in df.columns]
    if missing:
        cols = ", ".join(missing)
        raise CsvValidationError(
            f"colunas ausentes em '{schema.title}': {cols}. Cabeçalho esperado: "
            f"{schema.header_example}",
            code="missing_column",
            params={"col": cols, "dataset": schema.title},
        )

    if len(df) == 0:
        raise CsvValidationError(f"'{schema.title}': o arquivo não tem nenhuma linha de dados.")

    df = df[list(schema.required_names)].copy()

    for col in schema.columns:
        if col.kind == "datetime":
            parsed = pd.to_datetime(df[col.name], errors="coerce")
            if parsed.isna().any():
                example = df.loc[parsed.isna(), col.name].iloc[0]
                raise CsvValidationError(
                    f"'{schema.title}': coluna '{col.name}' tem valores que não são "
                    f"datas (ex.: '{example}').",
                    code="bad_dates",
                    params={"col": col.name, "value": example},
                )
            df[col.name] = parsed
        elif col.kind == "numeric":
            parsed = pd.to_numeric(df[col.name], errors="coerce")
            if parsed.isna().any():
                example = df.loc[parsed.isna(), col.name].iloc[0]
                raise CsvValidationError(
                    f"'{schema.title}': coluna '{col.name}' tem valores que não são "
                    f"números (ex.: '{example}').",
                    code="not_numeric",
                    params={"col": col.name, "value": example},
                )
            df[col.name] = parsed
        else:  # str
            df[col.name] = df[col.name].astype(str)

    return df


def load_csv(source: str | IO[bytes] | IO[str] | bytes, dataset_key: str) -> pd.DataFrame:
    """Lê e valida um CSV contra o schema do dataset.

    ``dataset_key`` em {"funnel", "cohort", "media", "sales"}. ``source`` pode
    ser caminho, objeto de arquivo (upload do Streamlit) ou bytes. Lança
    ``CsvValidationError`` com mensagem clara se o formato estiver errado.
    """
    if dataset_key not in SCHEMAS:
        raise ValueError(f"dataset desconhecido: {dataset_key}")
    schema = SCHEMAS[dataset_key]

    if isinstance(source, bytes):
        source = BytesIO(source)
    elif isinstance(source, str) and "\n" in source:
        source = StringIO(source)

    df = _read_raw(source)
    return _coerce_and_validate(df, schema)


def load_example(dataset_key: str) -> pd.DataFrame:
    """Carrega o CSV de exemplo embutido em ``data/`` para o dataset."""
    schema = SCHEMAS[dataset_key]
    path = os.path.join(DATA_DIR, schema.example_file)
    if not os.path.exists(path):
        raise CsvValidationError(
            f"exemplo '{schema.example_file}' não encontrado. "
            f"Rode: python data/generate_synthetic.py"
        )
    return load_csv(path, dataset_key)
