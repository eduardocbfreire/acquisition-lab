"""Gera CSVs sintéticos mas realistas para a acquisition-lab.

Roda offline e é determinístico (seed fixa), então o repositório funciona
logo após o clone, sem dados próprios. Cada arquivo exercita um bloco da spec:

- ``funnel.csv``     -> conversão por etapa com queda (bloco 2), inclui coortes
                        parciais perto do fim da janela.
- ``cohort.csv``     -> retenção semanal decaindo, matriz triangular (bloco 3).
- ``media_spend.csv``-> CAC com defasagem real de 7 dias e UM change point
                        plantado para a detecção encontrar (blocos 1 e 4).
- ``sales.csv``      -> receita e pedidos por usuário, positivamente
                        correlacionados, para o delta method (bloco 5).

Uso:
    python data/generate_synthetic.py
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# Âncora temporal fixa para manter os arquivos determinísticos.
END_DATE = datetime(2026, 5, 31)
SEED = 20260531
HERE = os.path.dirname(os.path.abspath(__file__))


# --------------------------------------------------------------------------- #
# Funil
# --------------------------------------------------------------------------- #
def generate_funnel(rng: np.random.Generator) -> pd.DataFrame:
    """Log de funil em formato longo: uma linha por (usuário, etapa atingida).

    Etapas ordenadas: visit -> signup -> activate -> purchase. As conversões
    caem a cada etapa. Usuários que entram perto do fim da janela ainda não
    tiveram tempo de comprar (coorte parcial), o que o módulo de funil marca.
    """
    n_users = 9000
    window_days = 180
    start = END_DATE - timedelta(days=window_days)

    # Tempo de entrada (visita) espalhado pela janela.
    entry_offsets = rng.uniform(0, window_days, size=n_users)
    entry_times = np.array([start + timedelta(days=float(o)) for o in entry_offsets])

    # Probabilidades de avanço passo a passo.
    p_signup = 0.42
    p_activate = 0.55
    p_purchase = 0.38

    # Atrasos típicos entre etapas (em dias).
    rows = []
    for i in range(n_users):
        uid = f"u{i:06d}"
        t_visit = entry_times[i]
        rows.append((uid, "visit", t_visit))

        if rng.random() > p_signup:
            continue
        t_signup = t_visit + timedelta(hours=float(rng.uniform(0, 48)))
        rows.append((uid, "signup", t_signup))

        if rng.random() > p_activate:
            continue
        t_activate = t_signup + timedelta(days=float(rng.exponential(2.0)))
        rows.append((uid, "activate", t_activate))

        # Compra leva tempo: usuários recentes podem não ter chegado lá ainda.
        delay_purchase = rng.exponential(9.0)
        t_purchase = t_activate + timedelta(days=float(delay_purchase))
        if rng.random() > p_purchase or t_purchase > END_DATE:
            continue
        rows.append((uid, "purchase", t_purchase))

    df = pd.DataFrame(rows, columns=["user_id", "step", "event_time"])
    df["event_time"] = pd.to_datetime(df["event_time"]).dt.floor("s")
    return df.sort_values(["user_id", "event_time"]).reset_index(drop=True)


# --------------------------------------------------------------------------- #
# Coorte / retenção
# --------------------------------------------------------------------------- #
def generate_cohort(rng: np.random.Generator) -> pd.DataFrame:
    """Log de atividade por usuário: user_id, signup_date, activity_date.

    Coorte = semana de signup. Cada usuário tem ao menos a atividade do
    período 0 (no signup); semanas seguintes seguem decaimento geométrico de
    retenção, até 12 semanas. Coortes recentes têm menos períodos observados
    (matriz triangular). Não imputamos nada: simplesmente não geramos linhas
    para períodos que ainda não aconteceram.
    """
    n_weeks = 22
    cohort_start = END_DATE - timedelta(weeks=n_weeks)
    base_retention = 0.55  # retenção da semana 1 sobre a coorte
    weekly_decay = 0.82  # cada semana retém ~82% da retenção anterior
    max_period = 12

    rows = []
    uid_counter = 0
    for w in range(n_weeks):
        signup_date = cohort_start + timedelta(weeks=w)
        cohort_size = int(rng.uniform(180, 320))
        # Períodos relativos observáveis para esta coorte (maturidade).
        weeks_observed = int((END_DATE - signup_date).days // 7)
        max_obs = min(max_period, weeks_observed)

        for _ in range(cohort_size):
            uid = f"c{uid_counter:06d}"
            uid_counter += 1
            # Período 0: atividade no dia do signup.
            rows.append((uid, signup_date, signup_date))

            ret = base_retention
            for period in range(1, max_obs + 1):
                if rng.random() < ret:
                    # Atividade em algum dia daquela semana relativa.
                    day_offset = period * 7 + int(rng.uniform(0, 7))
                    act_date = signup_date + timedelta(days=day_offset)
                    if act_date <= END_DATE:
                        rows.append((uid, signup_date, act_date))
                ret *= weekly_decay

    df = pd.DataFrame(rows, columns=["user_id", "signup_date", "activity_date"])
    df["signup_date"] = pd.to_datetime(df["signup_date"]).dt.normalize()
    df["activity_date"] = pd.to_datetime(df["activity_date"]).dt.normalize()
    return df.sort_values(["user_id", "activity_date"]).reset_index(drop=True)


# --------------------------------------------------------------------------- #
# Mídia vs resultado
# --------------------------------------------------------------------------- #
def generate_media(rng: np.random.Generator) -> pd.DataFrame:
    """Série diária: date, spend, conversions.

    O gasto tem sazonalidade semanal e ruído. As conversões respondem ao
    gasto com defasagem FIXA de 7 dias (conv[t] vem de spend[t-7]), o que a
    detecção de defasagem por correlação cruzada deve recuperar. Há UM change
    point plantado no CAC: a eficiência piora (CAC sobe ~45%) por volta do
    dia 165, para o PELT encontrar.

    A série tem ~37 semanas (259 dias) para que o CAC semanal ultrapasse o
    mínimo de 30 pontos exigido pela detecção, sem afrouxar esse parâmetro.
    """
    n_days = 259
    lag = 7
    start = END_DATE - timedelta(days=n_days - 1)
    dates = [start + timedelta(days=d) for d in range(n_days)]

    t = np.arange(n_days)
    weekly = 1.0 + 0.25 * np.sin(2 * np.pi * t / 7.0)
    trend = 1.0 + 0.0025 * t  # leve crescimento de investimento
    spend = 1800.0 * weekly * trend * rng.lognormal(0, 0.06, size=n_days)

    # CAC "verdadeiro" com um degrau plantado.
    cac_true = np.where(t < 165, 42.0, 61.0)
    cac_true = cac_true * rng.lognormal(0, 0.05, size=n_days)

    # Conversões respondem ao gasto defasado.
    conversions = np.zeros(n_days)
    for i in range(n_days):
        src = max(0, i - lag)
        conversions[i] = spend[src] / cac_true[i]
    conversions = np.maximum(0, conversions + rng.normal(0, 2.0, size=n_days))
    conversions = np.round(conversions).astype(int)

    df = pd.DataFrame(
        {
            "date": pd.to_datetime(dates).normalize(),
            "spend": np.round(spend, 2),
            "conversions": conversions,
        }
    )
    return df


# --------------------------------------------------------------------------- #
# Vendas / receita (delta method)
# --------------------------------------------------------------------------- #
def generate_sales(rng: np.random.Generator) -> pd.DataFrame:
    """Receita e pedidos por usuário: user_id, revenue, orders.

    A unidade de análise/agregação é o usuário. A métrica de razão é o ticket
    médio (AOV = receita total / pedidos totais). Receita e pedidos são
    positivamente correlacionados (mais pedidos -> mais receita), justamente o
    caso em que ignorar a covariância no delta method subestima a variância.
    """
    n_users = 4000
    # Pedidos por usuário: muitos com poucos pedidos, cauda longa.
    orders = rng.poisson(lam=1.8, size=n_users)

    # Valor por pedido com dispersão lognormal; usuários com mais pedidos
    # tendem a ter ticket levemente maior (heterogeneidade realista).
    rows = []
    for i in range(n_users):
        uid = f"s{i:06d}"
        n_ord = int(orders[i])
        if n_ord == 0:
            rows.append((uid, 0.0, 0))
            continue
        mean_ticket = 70.0 * (1.0 + 0.04 * n_ord)
        order_values = rng.lognormal(mean=np.log(mean_ticket), sigma=0.4, size=n_ord)
        rows.append((uid, float(np.round(order_values.sum(), 2)), n_ord))

    df = pd.DataFrame(rows, columns=["user_id", "revenue", "orders"])
    return df


# --------------------------------------------------------------------------- #
def main() -> None:
    rng = np.random.default_rng(SEED)
    datasets = {
        "funnel.csv": generate_funnel(rng),
        "cohort.csv": generate_cohort(rng),
        "media_spend.csv": generate_media(rng),
        "sales.csv": generate_sales(rng),
    }
    for name, df in datasets.items():
        path = os.path.join(HERE, name)
        df.to_csv(path, index=False)
        print(f"escrito {name}: {len(df):,} linhas -> {path}")


if __name__ == "__main__":
    main()
