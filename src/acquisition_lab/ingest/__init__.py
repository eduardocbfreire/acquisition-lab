"""Camada de ingestão: leitura e validação de CSVs."""

from .loaders import CsvValidationError, load_csv, load_example
from .schemas import SCHEMAS, DatasetSchema

__all__ = [
    "CsvValidationError",
    "load_csv",
    "load_example",
    "SCHEMAS",
    "DatasetSchema",
]
