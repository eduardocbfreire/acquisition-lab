# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/);
o projeto segue [versionamento semântico](https://semver.org/lang/pt-BR/).

## [0.1.0] - 2026-06-06

Primeira versão pública.

### Adicionado
- App Streamlit local e offline com seis abas: Visão Geral, Funil, Coorte,
  Mídia, Change Points e Vendas/Receita.
- **Funil** (bloco 2): conversão por etapa sobre usuários únicos, passo a passo
  e ponta a ponta, com IC de Wilson 95% e n absoluto; exclusão de coortes parciais.
- **Coorte** (bloco 3): matriz triangular de retenção por coorte × período
  relativo, sem imputação, com taxa, n e IC de Wilson por célula.
- **Mídia** (bloco 4): CAC semanal com defasagem estimada por correlação cruzada
  e change points marcados; rótulo de **CAC descritivo, não causal** em todo lugar
  que exibe CAC.
- **Change points** (bloco 1): PELT (ruptures) offline com penalidade estilo BIC,
  σ² robusto por MAD dos diffs, filtro de magnitude e teste de estabilidade.
- **Vendas/Receita** (bloco 5): ticket médio como métrica de razão com variância
  pelo delta method (termo de covariância incluído) e bootstrap opcional.
- Ingestão com validação de schema e mensagens de erro claras no upload.
- Dados sintéticos determinísticos em `data/` (gerador com seed fixa), incluindo
  um change point plantado no CAC e covariância positiva para o delta method.
- Tema visual em tons terrosos: `.streamlit/config.toml` para o chrome e
  `viz/theme.py` como fonte única da paleta e do template Plotly.
- Suíte de testes (pytest), um arquivo por bloco da spec.
- CI no GitHub Actions: ruff (lint + format) e pytest em Python 3.11.

[0.1.0]: https://github.com/OWNER/acquisition-lab/releases/tag/v0.1.0

