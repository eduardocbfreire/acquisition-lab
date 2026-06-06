"""Bloco 2 — Funil.

Conversão por etapa como proporção de USUÁRIOS ÚNICOS que avançam (nunca
eventos), passo a passo e ponta a ponta. Incerteza por IC de Wilson 95%,
com o n absoluto ao lado de cada taxa. Coortes parciais (quem entrou perto do
fim da janela e ainda não teve tempo de converter) são marcadas e excluídas
dos denominadores.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .stats import ProportionEstimate, wilson_proportion


@dataclass(frozen=True)
class FunnelStep:
    step: str
    users: int  # usuários únicos que atingiram esta etapa
    step_conversion: ProportionEstimate | None  # vs etapa anterior (None na 1ª)
    overall_conversion: ProportionEstimate  # vs etapa de entrada (ponta a ponta)


@dataclass(frozen=True)
class FunnelResult:
    steps: list[FunnelStep]
    n_entered: int
    n_excluded_immature: int  # usuários removidos por coorte parcial
    maturation_days: int
    window_end: pd.Timestamp

    @property
    def end_to_end(self) -> ProportionEstimate:
        return self.steps[-1].overall_conversion


def compute_funnel(
    df: pd.DataFrame,
    step_order: list[str],
    *,
    maturation_days: int = 14,
    window_end: pd.Timestamp | None = None,
    alpha: float = 0.05,
) -> FunnelResult:
    """Calcula conversões de funil com IC de Wilson por etapa e ponta a ponta.

    ``df`` em formato longo com colunas ``user_id``, ``step``, ``event_time``.
    ``step_order`` define a ordem das etapas (a primeira é a de entrada).

    Coortes parciais: usuários cujo evento de ENTRADA ocorreu depois de
    ``window_end - maturation_days`` são excluídos de todos os denominadores,
    porque ainda não tiveram tempo de percorrer o funil. O número de excluídos
    é reportado.

    Importante: cada etapa é contada por usuários únicos. O IC ponta a ponta é
    calculado direto sobre entrada e saída, NÃO multiplicando os IC das etapas
    (que não são independentes).
    """
    required = {"user_id", "step", "event_time"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"funil exige as colunas {sorted(required)}; faltam {sorted(missing)}")
    if not step_order:
        raise ValueError("step_order não pode ser vazio")

    df = df.copy()
    df["event_time"] = pd.to_datetime(df["event_time"])

    entry_step = step_order[0]
    if window_end is None:
        window_end = df["event_time"].max()
    cutoff = window_end - pd.Timedelta(days=maturation_days)

    # Tempo de entrada por usuário (primeiro evento na etapa de entrada).
    entry = df[df["step"] == entry_step].groupby("user_id")["event_time"].min().rename("entry_time")
    entered_users = set(entry.index)
    mature_users = set(entry[entry <= cutoff].index)
    n_excluded = len(entered_users) - len(mature_users)

    # Usuários únicos por etapa, restritos aos maduros.
    users_by_step: dict[str, set[str]] = {}
    for step in step_order:
        ids = set(df.loc[df["step"] == step, "user_id"].unique())
        users_by_step[step] = ids & mature_users

    n_entered = len(users_by_step[entry_step])

    steps: list[FunnelStep] = []
    for i, step in enumerate(step_order):
        n_here = len(users_by_step[step])
        if i == 0:
            step_conv = None
        else:
            n_prev = len(users_by_step[step_order[i - 1]])
            step_conv = wilson_proportion(n_here, n_prev, alpha=alpha)
        overall = wilson_proportion(n_here, n_entered, alpha=alpha)
        steps.append(
            FunnelStep(
                step=step,
                users=n_here,
                step_conversion=step_conv,
                overall_conversion=overall,
            )
        )

    return FunnelResult(
        steps=steps,
        n_entered=n_entered,
        n_excluded_immature=n_excluded,
        maturation_days=maturation_days,
        window_end=window_end,
    )


def infer_step_order(df: pd.DataFrame) -> list[str]:
    """Infere a ordem das etapas pela mediana do tempo de evento de cada uma."""
    order = (
        df.assign(event_time=pd.to_datetime(df["event_time"]))
        .groupby("step")["event_time"]
        .median()
        .sort_values()
    )
    return list(order.index)
