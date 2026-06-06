# acquisition-lab

<!-- Troque OWNER pelo seu usuário/organização do GitHub para os badges funcionarem. -->
[![CI](https://github.com/OWNER/acquisition-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/acquisition-lab/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-A98467.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-B85C38.svg)](https://www.python.org/)

Ferramenta **local** para analisar aquisição. Você sobe seus CSVs de funil,
coorte, mídia e vendas (ou usa os exemplos que já vêm no projeto) e vê conversão,
retenção, CAC e ticket médio. Toda taxa aparece com **a margem de incerteza
(intervalo de confiança) e o número de casos (n) ao lado** — a ideia é olhar a
faixa, não só o número solto. Roda em Streamlit, no seu computador, sem chave de
API nem serviço externo.

A interface fala **português e inglês** (botão no topo da barra lateral) e vem
num tema de **tons terrosos**. A paleta e o template dos gráficos ficam num só
lugar (`src/acquisition_lab/viz/theme.py`); os textos, num só dicionário
(`src/acquisition_lab/ui/i18n_pt.py` e `i18n_en.py`).

---

## Começando em 3 minutos

Para quem nunca usou. Você precisa de Python 3.11 ou mais novo.

1. Clone o projeto e entre na pasta:
   ```bash
   git clone https://github.com/OWNER/acquisition-lab.git
   cd acquisition-lab
   ```
2. Crie e ative um ambiente virtual.

   Linux ou macOS:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
   Windows (PowerShell):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Rode o app:
   ```bash
   streamlit run app.py
   ```
5. O navegador abre em http://localhost:8501. Se não abrir sozinho, cole esse endereço.
6. Na barra lateral, marque "usar exemplo" em cada conjunto e explore com os dados
   sintéticos que já vêm no projeto.
7. Para analisar seus próprios dados, desmarque "usar exemplo" e suba o CSV no
   formato da seção [Formato esperado de cada CSV](#formato-esperado-de-cada-csv).

Troque o idioma da interface (PT/EN) no topo da barra lateral.

### Outros comandos

Regerar os dados de exemplo (determinístico, mesma semente sempre):
```bash
python data/generate_synthetic.py
```
Rodar os testes:
```bash
pip install -r requirements-dev.txt
pytest
```

---

## Telas

São seis abas. Cada uma abre com um "Como ler esta tela?" para quem não é da área.

- **Visão geral**: os números principais lado a lado (conversão de ponta a ponta,
  retenção do 1º período, CAC médio, ticket médio), cada um com intervalo e n.
- **Funil**: conversão por etapa, contando pessoas (não eventos), com intervalo de
  Wilson 95%. Quem entrou há pouco e ainda não teve tempo de converter fica fora
  da conta, para não puxar as taxas para baixo.
- **Coorte**: matriz de retenção por grupo de entrada e tempo decorrido. Cada
  célula tem taxa, n e intervalo. Células ainda não observadas ficam em branco —
  não viram zero.
- **Mídia**: CAC por semana, já alinhando o atraso entre gasto e conversão, com os
  pontos de mudança marcados. Mostra sempre o aviso de que **o CAC é descritivo,
  não causal** (ver Metodologia).
- **Pontos de mudança** (change points): detecção interativa (PELT/ruptures) sobre
  séries dos dados — gasto, conversões, CAC, novos cadastros — com controles de
  sensibilidade, distância mínima e remoção de tendência.
- **Vendas**: ticket médio (receita ÷ pedidos) como métrica de razão, com a
  incerteza pelo **delta method** (já com o termo de covariância) e uma conferência
  opcional por bootstrap.

---

## Screenshots

As imagens da interface ficam em `docs/screenshots/`. Para gerar a sua: rode o
app, abra a aba "Visão geral" com os dados de exemplo e salve um print nessa pasta.

---

## Privacidade dos dados

Tudo roda na sua máquina. Os CSVs que você sobe ficam só na memória durante a
sessão: nada é gravado em disco nem enviado para nenhum serviço. Feche a aba e os
dados somem. Os únicos arquivos de dados no repositório são os exemplos sintéticos
de `data/`, criados por script.

---

## Formato esperado de cada CSV

A validação no upload checa colunas e tipos e dá mensagem de erro clara quando o
formato está errado. Cabeçalho e uma linha de exemplo por arquivo:

### Funil — `funnel.csv`
**O que é:** o caminho de cada pessoa pelas etapas do produto (visita, cadastro,
compra...).

Formato longo: uma linha por (usuário, etapa atingida). Denominadores são sempre
usuários únicos, nunca eventos.
```
user_id,step,event_time
u000001,signup,2026-01-15 09:32:10
```

### Coorte — `cohort.csv`
**O que é:** quando cada pessoa entrou e em que dias ela voltou a usar o produto.

Uma linha por atividade qualificadora do usuário. `signup_date` define a coorte;
`activity_date` marca o evento de retenção no período relativo.
```
user_id,signup_date,activity_date
c000001,2026-01-12,2026-02-09
```

### Mídia — `media_spend.csv`
**O que é:** quanto se gastou em mídia por dia e quantas aquisições vieram.

Série diária de gasto e aquisições atribuídas.
```
date,spend,conversions
2026-01-15,2243.10,52
```

### Vendas — `sales.csv`
**O que é:** quanto cada pessoa gastou e quantos pedidos fez.

Uma linha por usuário (unidade de agregação), com receita e número de pedidos.
```
user_id,revenue,orders
s000001,165.56,2
```

---

## Metodologia

Os métodos abaixo são a fonte da verdade do projeto. Cada bloco é um módulo de
análise puro em `src/acquisition_lab/analysis/`, testável sem subir o app.

### 1. Change points (`changepoints.py`)
PELT (Pruned Exact Linear Time) via **ruptures**, modo offline, segmentação
múltipla. Custo padrão `l2` (mudança de nível/média); `normal` (variância) e
`linear` (tendência) como opções. Penalidade estilo BIC, proporcional a `log(n)`:
`beta = k · d · sigma2 · log(n)`, com `d=1` (univariada), `sigma2` estimado de
forma robusta pela MAD dos primeiros diffs e `k=1.0` por padrão. Defaults:
`min_size=7` (diário; 4 para semanal), `jump=1`, série mínima de 30 pontos para
habilitar a detecção. Defesas contra excesso de pontos: penalidade BIC, `min_size`,
filtro de magnitude mínima (descarta quebras com salto de média < 1 MAD) e teste
de estabilidade (re-roda com `k=1.5` e mantém só os pontos persistentes). Para
séries com tendência forte, há opção de detrend antes do `l2` ou uso do custo
`linear`.

### 2. Funil (`funnel.py`)
Conversão por etapa como proporção de **usuários únicos** que avançam (passo a
passo e ponta a ponta), nunca eventos. Incerteza por **IC de Wilson** (score) 95%
via `statsmodels.stats.proportion.proportion_confint(method="wilson")`, nunca Wald.
O n absoluto acompanha cada taxa. O IC ponta a ponta é calculado direto sobre
entrada e saída — não é o produto dos IC das etapas (que não são independentes).
Coortes parciais (quem entrou perto do fim da janela) são excluídas dos
denominadores.

### 3. Coorte / retenção (`cohort.py`)
Coorte definida pelo período de aquisição (semana de signup por padrão); retenção
em períodos relativos desde a aquisição (0 a 12, ajustável). Célula =
`retidos_n / tamanho_da_coorte`, com taxa, n e IC de Wilson 95%. Matriz triangular:
coortes recentes têm menos períodos observados, e células não maduras **não são
imputadas** (ficam ausentes). Não se comparam células de maturidades diferentes,
e o tempo é sempre relativo à aquisição, nunca calendário.

### 4. Mídia vs resultado (`media.py`)
`CAC(t) = gasto / aquisições atribuídas`, agregado por semana, com defasagem fixa
entre gasto e conversão. A defasagem é estimada por **correlação cruzada** (teto de
30 dias) e as aquisições são deslocadas para trás antes da divisão; a defasagem
usada é sempre reportada. A detecção de change points do bloco 1 roda sobre a série
de CAC.

> **CAC é descritivo, não causal.** O CAC calculado de conversões atribuídas está
> contaminado por confundimento: demanda e sazonalidade movem tanto o gasto quanto
> as conversões. Atribuição **não** é incrementalidade. Medir incrementalidade
> exige experimento geográfico ou controle sintético, fora do escopo de uma análise
> descritiva de CSV. O app exibe esse rótulo em todo lugar que mostra CAC, e ele
> não deve ser removido nem suavizado.

### 5. Métricas de razão (`ratio.py`, `stats.py`)
Variância de razões (R = X/Y) pelo **delta method**, usada na aba Vendas para o
ticket médio (AOV = receita total / pedidos totais). O denominador é variável
aleatória, então a variância considera variância do numerador, do denominador **e
a covariância** entre eles, na unidade de agregação correta (o usuário):

```
var(R) ≈ (1 / mean_y²) · ( var_x − 2·R·cov_xy + R²·var_y ) / n
```

IC 95% como `R ± 1.96·sqrt(var(R))`. Receita e pedidos costumam ser positivamente
correlacionados; ignorar a covariância (tratar o denominador como constante) dá um
IC enviesado. Bootstrap (10.000 reamostragens, reamostrando o usuário inteiro)
fica disponível como validação opcional via toggle, não como método primário.

---

## Arquitetura

```
acquisition-lab/
├── app.py                       # entrypoint Streamlit (só monta as abas)
├── data/
│   ├── generate_synthetic.py    # gerador determinístico dos exemplos
│   └── *.csv                    # exemplos sintéticos
├── src/acquisition_lab/
│   ├── ingest/                  # leitura + validação de CSV (schemas, loaders)
│   ├── analysis/                # funções puras, um módulo por bloco da spec
│   ├── viz/                     # figuras plotly puras
│   └── ui/                      # camada Streamlit (única que importa streamlit)
└── tests/                       # um arquivo de teste por bloco
```

As funções de análise são puras (recebem DataFrame, devolvem resultado) e
separadas da camada Streamlit, então dá para testar tudo sem subir o app.

## Bibliotecas

pandas, numpy (ingestão e manipulação); ruptures (PELT); statsmodels (IC de Wilson,
ajuste de tendência); scipy (distribuições, estatística); streamlit (interface
local); plotly (gráficos interativos).

## Licença

MIT — veja [LICENSE](LICENSE).
