"""acquisition-lab: análise de aquisição offline com detecção de change points.

Pacote organizado em três camadas:

- ``ingest``: leitura e validação de CSVs.
- ``analysis``: funções puras (DataFrame -> resultado), uma por bloco da spec.
- ``viz``: funções puras (resultado -> figura plotly).

A camada Streamlit vive em ``ui`` e é a única que importa ``streamlit``.
"""

__version__ = "0.1.0"
