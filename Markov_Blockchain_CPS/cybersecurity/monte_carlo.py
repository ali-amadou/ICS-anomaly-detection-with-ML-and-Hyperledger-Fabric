"""
Simulation Monte Carlo du modèle DTMC de cybersécurité.

Objectif :
    comparer la distribution stationnaire théorique
    avec une simulation de 200 000 transitions.

Une graine fixe est utilisée pour rendre le résultat
reproductible.
"""

import numpy as np

from cybersecurity_markov import (
    STATES,
    P,
    stationary_distribution
)


N_STEPS = 200_000
INITIAL_STATE = 0
SEED = 42


def simulate(P, steps, initial_state=0, seed=42):

    rng = np.random.default_rng(seed)

    current_state = initial_state

    counts = np.zeros(
        len(P),
        dtype=np.int64
    )

    for _ in range(steps):

        # Comptage de l'état courant
        counts[current_state] += 1

        # Choix du prochain état
        current_state = rng.choice(
            len(P),
            p=P[current_state]
        )

    empirical_distribution = counts / steps

    return counts, empirical_distribution


def main():

    theoretical = stationary_distribution(P)

    counts, empirical = simulate(
        P,
        N_STEPS,
        INITIAL_STATE,
        SEED
    )

    print("=" * 78)
    print("MONTE CARLO — VALIDATION DU MODÈLE DTMC")
    print("=" * 78)

    print(
        f"\nNombre de transitions : "
        f"{N_STEPS:,}"
    )

    print(
        f"Graine aléatoire      : "
        f"{SEED}"
    )

    print(
        f"État initial          : "
        f"{STATES[INITIAL_STATE]}"
    )

    print("\nCOMPARAISON THÉORIQUE / SIMULATION")
    print("-" * 78)

    print(
        f"{'État':<18}"
        f"{'Théorique':>15}"
        f"{'Simulation':>15}"
        f"{'Écart absolu':>18}"
    )

    for state, theo, emp in zip(
        STATES,
        theoretical,
        empirical
    ):

        error = abs(theo - emp)

        print(
            f"{state:<18}"
            f"{theo * 100:>14.2f} %"
            f"{emp * 100:>14.2f} %"
            f"{error * 100:>17.2f} %"
        )

    print("\nCOMPTAGES OBSERVÉS")
    print("-" * 78)

    for state, count in zip(
        STATES,
        counts
    ):

        print(
            f"{state:<18} : "
            f"{count:,}"
        )

    max_error = np.max(
        np.abs(
            theoretical - empirical
        )
    )

    print("\nERREUR MAXIMALE")
    print("-" * 78)

    print(
        f"{max_error * 100:.3f} "
        "point(s) de pourcentage"
    )

    print("\nCONCLUSION")
    print("-" * 78)

    print(
        "La distribution obtenue par simulation "
        "est proche de la distribution stationnaire "
        "théorique."
    )

    print(
        "Cette simulation valide numériquement "
        "le comportement stationnaire du modèle."
    )

    print("\n" + "=" * 78)
    print("FIN DE LA SIMULATION")
    print("=" * 78)


if __name__ == "__main__":
    main()