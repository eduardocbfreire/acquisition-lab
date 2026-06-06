"""Strings da interface em português. Único lugar com texto PT visível.

A ressalva de CAC é importada da camada de análise para não duplicar a fonte
da verdade (o teste garante que aquele texto não muda).
"""

from __future__ import annotations

from ..analysis.media import CAC_DESCRIPTIVE_DISCLAIMER

PT: dict[str, str] = {
    # App / cabeçalho
    "app.title": "Acquisition Lab",
    "app.caption": "Análise de aquisição local: funil, coorte, mídia e vendas. "
    "Toda taxa vem com margem de incerteza e o número de casos.",
    # Sidebar
    "sidebar.data_title": "Dados",
    "sidebar.data_caption": "Suba seus arquivos CSV ou use os dados de exemplo. "
    "Tudo roda no seu computador.",
    "sidebar.use_example": "usar exemplo",
    "sidebar.upload_label": "CSV de {name}",
    "sidebar.upload_help": "Cabeçalho esperado: {header}",
    "sidebar.rows_upload": "{n} linhas carregadas.",
    "sidebar.rows_example": "{n} linhas (exemplo).",
    "sidebar.err_csv": "Problema no CSV de {name}: {detail}",
    "sidebar.err_unexpected": "Erro inesperado ao ler {name}: {detail}",
    # Textos embutidos do uploader do Streamlit, traduzidos via CSS
    "uploader.drag": "Arraste e solte o arquivo aqui",
    "uploader.limit": "Limite de 200 MB por arquivo • CSV",
    "uploader.browse": "Procurar arquivos",
    # Nomes dos conjuntos de dados
    "ds.funnel": "Funil",
    "ds.cohort": "Coorte",
    "ds.media": "Mídia",
    "ds.sales": "Vendas",
    # Abas
    "tab.overview": "Visão geral",
    "tab.funnel": "Funil",
    "tab.cohort": "Coorte",
    "tab.media": "Mídia",
    "tab.changepoints": "Pontos de mudança",
    "tab.sales": "Vendas",
    # Comuns
    "common.how_to_read": "Como ler esta tela?",
    "common.learn_more": "Para entender mais",
    "common.ci_n": "Intervalo de 95% [{lo}, {hi}] · n = {n} ({count} de {total})",
    "common.ci_n_simple": "Intervalo de 95% [{lo}, {hi}] · n = {n}",
    "common.cac_disclaimer": CAC_DESCRIPTIVE_DISCLAIMER,
    "common.missing_data": "Ainda não há dados de {name}. Na barra lateral, marque "
    '"usar exemplo" ou suba um CSV no formato certo.',
    "common.spinner_cac": "Procurando pontos de mudança no CAC…",
    # Visão geral
    "overview.caption": "Os números principais de cada tela, lado a lado. "
    "Cada taxa vem com a margem de incerteza e o número de casos.",
    "overview.help": "Esta tela resume tudo num lugar só. Cada cartão mostra um "
    "número e, abaixo, o intervalo de 95% — a faixa onde o valor real "
    "provavelmente está. Quanto mais estreita a faixa, mais confiança no número. "
    "O n é quantas pessoas ou casos entraram na conta: n baixo, desconfie.",
    "overview.no_data": "Nenhum dado carregado. Use a barra lateral para marcar "
    '"usar exemplo" ou subir seus CSVs. O projeto já vem com dados de exemplo.',
    "overview.funnel_label": "Funil",
    "overview.metric.e2e": "Conversão de ponta a ponta",
    "overview.metric.e2e.help": "De cada 100 pessoas que entraram, quantas chegaram "
    "ao fim. O intervalo mostra a margem de incerteza: quanto mais estreito, mais "
    "confiável.",
    "overview.retention_label": "Retenção (1º período)",
    "overview.metric.retention": "Retenção média no 1º período",
    "overview.metric.retention.help": "De quem entrou, qual fração voltou no período "
    "seguinte, em média. Acompanha o intervalo de incerteza.",
    "overview.retention_caption": "média de {n} coortes maduras",
    "overview.media_label": "Mídia (CAC)",
    "overview.metric.cac": "Custo por aquisição (CAC)",
    "overview.metric.cac.help": "Quanto se gastou em média para conseguir uma "
    "aquisição. É um retrato do que aconteceu, não a prova de que a mídia causou o "
    "resultado.",
    "overview.cac_caption": "defasagem {lag}d · {n} pontos de mudança",
    "overview.sales_label": "Vendas (ticket médio)",
    "overview.metric.aov": "Ticket médio",
    "overview.metric.aov.help": "Quanto rende cada pedido, em média. O intervalo é a "
    "margem de incerteza dessa média.",
    # Funil
    "funnel.caption": "Para cada etapa, a fração de pessoas que avança. Conta pessoas "
    "(não eventos) e mostra a margem de incerteza ao lado.",
    "funnel.help": "O funil mostra quantas pessoas passam de uma etapa para a "
    "seguinte. Cada barra é uma etapa; a conversão é quantas pessoas seguiram "
    "adiante. O intervalo de 95% é a margem de incerteza, e o n é quantas pessoas "
    "entraram na conta. Quem chegou há pouco e ainda não teve tempo de avançar fica "
    "de fora, para não puxar as taxas para baixo.",
    "funnel.steps_label": "Ordem das etapas (entrada → saída)",
    "funnel.steps_help": "A primeira etapa é a porta de entrada; as taxas de ponta a "
    "ponta usam ela como base.",
    "funnel.maturation_label": "Tempo de espera (dias)",
    "funnel.maturation_help": "Quem entrou há menos dias que isso ainda não teve tempo "
    "de converter e fica de fora da conta.",
    "funnel.min_steps_warn": "Escolha pelo menos 2 etapas.",
    "funnel.excluded_info": "{n} pessoas que entraram nos últimos {days} dias ficaram "
    "de fora: ainda não tiveram tempo de avançar.",
    "funnel.subheader_e2e": "Da entrada até o fim",
    "funnel.e2e_caption": "Calculado direto entre a entrada e a saída. Não dá para "
    "multiplicar as taxas das etapas: elas não são independentes.",
    "funnel.subheader_detail": "Etapa por etapa",
    "funnel.col.step": "etapa",
    "funnel.col.users": "pessoas",
    "funnel.col.conv_prev": "conversão vs etapa anterior",
    "funnel.col.ci_prev": "intervalo 95% vs anterior",
    "funnel.col.conv_e2e": "conversão acumulada",
    # Coorte
    "cohort.caption": "Agrupa as pessoas por quando entraram e acompanha quantas "
    "voltam ao longo do tempo. Cada célula tem taxa, número de casos e margem de "
    "incerteza.",
    "cohort.help": "Uma coorte é um grupo de pessoas que entrou no mesmo período "
    "(por padrão, na mesma semana). Cada linha é uma coorte; cada coluna é quanto "
    "tempo passou desde a entrada. A cor mostra a fração que continuou ativa. "
    "Grupos que entraram há pouco têm menos colunas preenchidas — as células em "
    "branco ainda não aconteceram, não são zero.",
    "cohort.gran_label": "Agrupar por",
    "cohort.gran.W": "Semana",
    "cohort.gran.D": "Dia",
    "cohort.gran.M": "Mês",
    "cohort.periods_label": "Períodos (0 a N)",
    "cohort.warn": "Não compare células com idades diferentes: grupos recentes têm "
    "menos tempo observado. As células em branco não foram observadas ainda — não "
    "valem zero.",
    "cohort.sizes_subheader": "Tamanho de cada coorte",
    "cohort.col.cohort": "coorte",
    "cohort.col.size": "tamanho",
    # Mídia
    "media.caption": "Custo por aquisição (CAC) semana a semana, com o atraso entre "
    "gastar e converter já corrigido, e os pontos onde o custo mudou de patamar.",
    "media.help": "O CAC é quanto se gasta para conseguir cada aquisição. Como a "
    "conversão costuma vir alguns dias depois do gasto, alinhamos os dois antes de "
    "dividir. Os marcadores apontam semanas em que o custo mudou de patamar. "
    "Atenção: isto descreve o que aconteceu, não prova que a mídia causou o "
    "resultado.",
    "media.auto_lag_label": "Descobrir o atraso automaticamente (sugestão: {lag} dias)",
    "media.manual_lag_label": "Atraso manual (dias)",
    "media.smooth_label": "Suavização (semanas)",
    "media.metric.lag": "Atraso usado",
    "media.metric.lag.value": "{lag} dias",
    "media.metric.lag.help": "Quantos dias a conversão costuma demorar depois do "
    "gasto. Alinhamos os dois por esse atraso antes de calcular o custo.",
    "media.metric.cac": "CAC médio",
    "media.metric.cac.help": "Custo médio por aquisição no período. Descritivo: não "
    "é prova de causa.",
    "media.metric.cps": "Pontos de mudança",
    "media.metric.cps.help": "Quantas vezes o custo por aquisição mudou de patamar de "
    "forma consistente.",
    "media.cps_found": "Semanas em que o custo mudou de patamar:",
    # Pontos de mudança
    "cp.caption": "Encontra automaticamente os momentos em que uma série muda de "
    "patamar, de variação ou de tendência.",
    "cp.help": "Para que serve: descobrir QUANDO uma métrica mudou de patamar — por "
    "exemplo, o CAC que sobe de degrau depois de certa semana — de forma automática, "
    "sem você escolher a data no olho. O método separa a mudança de verdade do "
    "sobe-e-desce normal: ignora saltos pequenos e só mantém o que se repete quando o "
    "critério aperta. Ajuste os controles para deixar a busca mais ou menos sensível.",
    "cp.no_data": "Carregue dados de Mídia ou Coorte para ter séries para analisar.",
    "cp.series_label": "Série",
    "cp.series.spend": "Mídia · gasto por dia",
    "cp.series.conv": "Mídia · conversões por dia",
    "cp.series.cac": "Mídia · CAC por semana",
    "cp.series.signups": "Coorte · novos cadastros por dia",
    "cp.cost_label": "O que pode ter mudado",
    "cp.cost.l2": "O patamar (média)",
    "cp.cost.normal": "A variação",
    "cp.cost.linear": "A tendência",
    "cp.cost_help": "l2 detecta mudança de nível médio; normal, de variância; linear, "
    "de tendência.",
    "cp.k_label": "Sensibilidade",
    "cp.k_help": "Valores maiores = menos pontos, só as mudanças mais óbvias. Comece em "
    "1.0 e aumente se vier ruído.",
    "cp.minsize_label": "Distância mínima entre pontos",
    "cp.minsize_help": "Número mínimo de pontos (dias ou semanas, conforme a série) "
    "entre duas mudanças. Evita marcar oscilação curta como mudança.",
    "cp.detrend_label": "Remover tendência antes",
    "cp.detrend_help": "Remove a tendência de fundo antes de procurar degraus. Use "
    "quando a série sobe ou desce continuamente.",
    "cp.metric.cps": "Pontos de mudança",
    "cp.metric.sigma": "Ruído estimado",
    "cp.metric.sigma.help": "O quanto a série treme normalmente. Serve de régua para "
    "decidir o que é mudança de verdade.",
    "cp.metric.pen": "Exigência (penalidade)",
    "cp.metric.pen.help": "Quanto a série precisa mudar para valer um ponto novo. "
    "Mais alto = mais conservador.",
    "cp.dropped_mag": "Ignorados por salto pequeno: {n}",
    "cp.dropped_unstable": "Ignorados por não se repetirem num critério mais " "exigente: {n}",
    "cp.min_points": "Precisa de pelo menos {min} pontos; esta série tem {n}.",
    "cp.spinner": "Procurando pontos de mudança…",
    "cp.ref.ruptures": "Documentação do **ruptures**, a biblioteca por trás da "
    "detecção — vale ver os exemplos e parâmetros "
    "([ruptures-docs](https://centre-borelli.github.io/ruptures-docs/)).",
    "cp.ref.truong": "Truong, Oudre & Vayatis (2020), *Selective review of offline "
    "change point detection methods* — um bom panorama de todos os métodos.",
    "cp.ref.killick": "Killick, Fearnhead & Eckley (2012) — o artigo do PELT, o "
    "algoritmo exato que roda aqui por baixo.",
    # Vendas
    "sales.caption": "Ticket médio (receita dividida por pedidos) com a margem de "
    "incerteza calculada do jeito certo, levando em conta que os dois variam juntos.",
    "sales.help": "O ticket médio é a receita total dividida pelos pedidos totais. "
    "Como receita e número de pedidos variam de pessoa para pessoa e andam juntos, "
    "a margem de incerteza precisa levar isso em conta — senão fica errada. A "
    "reamostragem (bootstrap) é uma conferência opcional do mesmo número.",
    "sales.boot_label": "Conferir por reamostragem (bootstrap, 10.000 vezes)",
    "sales.boot_help": "Refaz a conta sorteando pessoas com repetição, como uma "
    "segunda opinião sobre a margem. Opcional.",
    "sales.metric.aov": "Ticket médio (receita / pedidos)",
    "sales.metric.aov.help": "Quanto rende cada pedido, em média. O intervalo de 95% "
    "é a margem de incerteza.",
    "sales.metric.se": "Margem (forma correta)",
    "sales.metric.se.help": "Tamanho típico do erro da estimativa, levando em conta "
    "que receita e número de pedidos variam juntos. É a margem em que confiar.",
    "sales.metric.se_naive": "Margem (forma ingênua)",
    "sales.metric.se_naive.help": "O que daria tratando o número de pedidos como fixo, "
    "ignorando que receita e pedidos variam juntos. Como costumam ser positivamente "
    "correlacionados, essa margem sai distorcida. Está aqui só para mostrar o tamanho "
    "do erro de ignorar isso.",
    "sales.info_cov_reduces": "Receita e pedidos andam juntos: quem faz mais pedidos "
    "gasta mais. Levar isso em conta deixa a margem mais estreita do que a forma "
    "ingênua sugere. Em outros dados pode ser o contrário — o importante é não "
    "tratar o nº de pedidos como fixo.",
    "sales.info_cov_generic": "O cálculo leva em conta que receita e pedidos variam "
    "juntos. Tratar o nº de pedidos como fixo dá uma margem errada.",
    "sales.boot_caption": "Reamostragem: {p}, intervalo de 95% [{lo}, {hi}].",
    "sales.dist_caption": "A distribuição costuma ser assimétrica (muitos tickets "
    "baixos, poucos altos) — por isso a média vem com intervalo, não sozinha.",
    "sales.boot_dist_caption": "Se as duas faixas praticamente coincidem, o delta "
    "method está validado.",
    "sales.sample_subheader": "Uma amostra dos dados",
    "sales.ref.delta": "Delta method para razões: qualquer texto de *survey statistics* "
    "sobre 'ratio estimators' explica por que o denominador também conta.",
    "sales.ref.bootstrap": "Efron & Tibshirani, *An Introduction to the Bootstrap* — a "
    "leitura clássica do método de reamostragem usado na conferência.",
    # Gráficos (viz)
    "viz.funnel.title": "Funil — {entered} entradas consideradas " "({excluded} parciais de fora)",
    "viz.funnel.n": "n = {n}",
    "viz.funnel.conv_prev": "{rate} vs etapa anterior",
    "viz.funnel.ci": "intervalo 95% [{lo}, {hi}]",
    "viz.funnel.step_title": "Conversão entre etapas (intervalo de 95%)",
    "viz.funnel.step_yaxis": "conversão",
    "viz.cohort.title": "Retenção por coorte (agrupada por {gran})",
    "viz.cohort.xaxis": "períodos desde a entrada",
    "viz.cohort.yaxis": "coorte (quando a pessoa entrou)",
    "viz.cohort.hover": "coorte %{y} · período %{x}<br>retenção %{z:.1%}<br>"
    "intervalo 95% [%{customdata[0]:.1%}, %{customdata[1]:.1%}]<br>"
    "%{customdata[2]:.0f} de %{customdata[3]:.0f} pessoas<extra></extra>",
    "viz.media.title": "CAC por semana — atraso de {lag} dias",
    "viz.media.xaxis": "semana",
    "viz.media.yaxis": "CAC (gasto / aquisições)",
    "viz.media.series_raw": "CAC por semana",
    "viz.media.series_smooth": "CAC suavizado",
    "viz.changepoint_marker": "ponto de mudança",
    "viz.cp.xaxis": "período",
    "viz.cp.subtitle": "PELT/{model} · exigência={pen} · ruído≈{sigma} · " "distância mín.={min}",
    "viz.cp.disabled": "{message}",
    "viz.cp.segment_mean": "média {mean}",
    "viz.sales.title": "Ticket médio = {ratio} · intervalo de 95% por método",
    "viz.sales.compare_xaxis": "ticket médio (R$)",
    "viz.sales.compare_hover": "Ticket {ratio} · margem ±{half}",
    "viz.sales.method.delta": "Delta method (com covariância)",
    "viz.sales.method.naive": "Ingênua (ignora covariância)",
    "viz.sales.dist.title": "Distribuição do ticket por usuário",
    "viz.sales.dist.xaxis": "ticket por usuário (R$)",
    "viz.sales.dist.yaxis": "usuários",
    "viz.sales.dist.aov_line": "ticket médio",
    "viz.sales.boot.title": "Distribuição das estimativas reamostradas",
    "viz.sales.boot.xaxis": "ticket médio reamostrado (R$)",
    "viz.sales.boot.yaxis": "reamostragens",
    "viz.sales.boot.band": "IC 95% (bootstrap)",
    "viz.sales.boot.delta": "IC 95% (delta method)",
}
