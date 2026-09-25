"""
Modèle CTMC — Disponibilité d'une infrastructure Blockchain-CPS/PLC.

États :
    Disponible
    Dégradé
    Indisponible

Paramètres issus du cahier des charges de l'Exercice 3.
"""

import numpy as np


STATES = [
    "Disponible",
    "Dégradé",
    "Indisponible"
]

# Matrice génératrice Q, taux en transitions par heure
Q = np.array([
    [-0.06, 0.05, 0.01],
    [ 0.20,-0.25, 0.05],
    [ 0.50, 0.00,-0.50]
])


def validate_generator(Q):
    """Vérifie que Q est bien une matrice génératrice CTMC."""

    # La somme de chaque ligne doit être nulle
    if not np.allclose(Q.sum(axis=1), 0):
        raise ValueError(
            "Erreur : chaque ligne de Q doit avoir une somme nulle."
        )

    # Les éléments hors diagonale sont des taux positifs
    for i in range(len(Q)):
        for j in range(len(Q)):
            if i != j and Q[i, j] < 0:
                raise ValueError(
                    "Erreur : les taux hors diagonale doivent être positifs."
                )


def stationary_distribution(Q):
    """
    Calcule la distribution stationnaire pi telle que :

        pi Q = 0

    avec :

        somme(pi) = 1
    """

    A = Q.T.copy()
    b = np.zeros(len(Q))

    # Remplacement d'une équation par la contrainte de normalisation
    A[-1, :] = 1
    b[-1] = 1

    pi = np.linalg.solve(A, b)

    return pi


def mean_holding_times(Q):
    """
    Calcule le temps moyen de séjour dans chaque état.

    Pour un état i :
        temps moyen = 1 / |q_ii|
    """

    return np.array([
        1 / abs(Q[i, i])
        for i in range(len(Q))
    ])


def main():

    print("=" * 70)
    print("CTMC — DISPONIBILITÉ BLOCKCHAIN-CPS/PLC")
    print("=" * 70)

    validate_generator(Q)

    print("\nÉtats du modèle :")

    for i, state in enumerate(STATES):
        print(f"  {i} : {state}")

    print("\nMatrice génératrice Q")
    print("-" * 70)

    print(f"{'':20}", end="")
    for state in STATES:
        print(f"{state:>17}", end="")
    print()

    for state, row in zip(STATES, Q):
        print(f"{state:20}", end="")
        for value in row:
            print(f"{value:17.3f}", end="")
        print()

    # Distribution stationnaire
    pi = stationary_distribution(Q)

    print("\nDISTRIBUTION STATIONNAIRE")
    print("-" * 70)

    for state, probability in zip(STATES, pi):
        print(
            f"{state:20} : "
            f"{probability * 100:6.2f} %"
        )

    print(f"\nSomme = {pi.sum():.6f}")

    # Temps moyens de séjour
    holding_times = mean_holding_times(Q)

    print("\nTEMPS MOYEN DE SÉJOUR")
    print("-" * 70)

    for state, time in zip(STATES, holding_times):
        print(
            f"{state:20} : "
            f"{time:.2f} heure(s)"
        )

    # MTTR
    repair_rate = 0.50
    mttr = 1 / repair_rate

    print("\nPARAMÈTRE DE RÉPARATION")
    print("-" * 70)

    print(f"Taux de réparation : {repair_rate:.2f} / heure")
    print(f"MTTR               : {mttr:.2f} heure(s)")

    # Interprétation
    print("\nINTERPRÉTATION")
    print("-" * 70)

    print(
        f"Sous les paramètres retenus, l'infrastructure est "
        f"Disponible pendant environ {pi[0] * 100:.2f} % du temps."
    )

    print(
        f"L'état Dégradé représente environ {pi[1] * 100:.2f} % "
        f"et l'état Indisponible {pi[2] * 100:.2f} %."
    )

    print("\n" + "=" * 70)
    print("FIN DU CALCUL")
    print("=" * 70)


if __name__ == "__main__":
    main()