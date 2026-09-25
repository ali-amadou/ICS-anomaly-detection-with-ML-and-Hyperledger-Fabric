"""
DTMC — Modèle probabiliste de cybersécurité
pour une infrastructure Blockchain-CPS/PLC.

États :
    Normal
    Suspect
    Compromis
    Isolé

Les probabilités sont celles du cahier des charges
de l'Exercice 3.
"""

import numpy as np


STATES = [
    "Normal",
    "Suspect",
    "Compromis",
    "Isolé"
]


# Matrice de transition P
#
#             Normal  Suspect  Compromis  Isolé
#
# Normal       0.97     0.03      0.00     0.00
# Suspect      0.60     0.10      0.30     0.00
# Compromis    0.00     0.00      0.20     0.80
# Isolé        0.70     0.00      0.00     0.30

P = np.array([
    [0.97, 0.03, 0.00, 0.00],
    [0.60, 0.10, 0.30, 0.00],
    [0.00, 0.00, 0.20, 0.80],
    [0.70, 0.00, 0.00, 0.30]
])


def validate_matrix(P):
    """
    Vérifie que P est une matrice de transition valide.
    """

    if np.any(P < 0):
        raise ValueError(
            "Les probabilités doivent être positives ou nulles."
        )

    if not np.allclose(P.sum(axis=1), 1.0):
        raise ValueError(
            "Chaque ligne de P doit avoir une somme égale à 1."
        )


def stationary_distribution(P):
    """
    Calcule la distribution stationnaire pi :

        pi P = pi

    avec :

        somme(pi) = 1
    """

    A = P.T - np.eye(P.shape[0])

    # Contrainte de normalisation
    A[-1, :] = 1.0

    b = np.zeros(P.shape[0])
    b[-1] = 1.0

    pi = np.linalg.solve(A, b)

    return pi


def mean_return_to_normal(P):
    """
    Temps moyen de récurrence de l'état Normal.

    Pour une chaîne ergodique :
        T_Normal = 1 / pi_Normal
    """

    pi = stationary_distribution(P)

    return 1.0 / pi[0]


def main():

    validate_matrix(P)

    pi = stationary_distribution(P)

    return_time = mean_return_to_normal(P)

    print("=" * 72)
    print("DTMC — CYBERSÉCURITÉ BLOCKCHAIN-CPS/PLC")
    print("=" * 72)

    print("\nÉtats du modèle")
    print("-" * 72)

    for i, state in enumerate(STATES):
        print(f"{i} : {state}")

    print("\nMATRICE DE TRANSITION P")
    print("-" * 72)

    print(
        f"{'':18}"
        f"{'Normal':>14}"
        f"{'Suspect':>14}"
        f"{'Compromis':>14}"
        f"{'Isolé':>14}"
    )

    for state, row in zip(STATES, P):

        print(
            f"{state:<18}"
            f"{row[0]:>14.2f}"
            f"{row[1]:>14.2f}"
            f"{row[2]:>14.2f}"
            f"{row[3]:>14.2f}"
        )

    print("\nDISTRIBUTION STATIONNAIRE")
    print("-" * 72)

    for state, probability in zip(STATES, pi):

        print(
            f"{state:<18} : "
            f"{probability * 100:6.2f} %"
        )

    print(
        f"\nSomme des probabilités : "
        f"{pi.sum():.6f}"
    )

    print("\nTEMPS MOYEN DE RÉCURRENCE DE L'ÉTAT NORMAL")
    print("-" * 72)

    print(
        f"{return_time:.2f} cycle(s)"
    )

    print("\nINDICATEUR DE COMPROMISSION")
    print("-" * 72)

    print(
        f"Probabilité stationnaire de Compromis : "
        f"{pi[2] * 100:.2f} %"
    )

    print(
        f"Probabilité stationnaire d'Isolé : "
        f"{pi[3] * 100:.2f} %"
    )

    print("\nINTERPRÉTATION")
    print("-" * 72)

    print(
        "Sous les paramètres retenus, le système reste "
        f"dans l'état Normal environ {pi[0] * 100:.2f} % "
        "du temps."
    )

    print(
        "L'état Compromis représente environ "
        f"{pi[2] * 100:.2f} % du régime stationnaire."
    )

    print(
        "L'état Isolé représente environ "
        f"{pi[3] * 100:.2f} % du régime stationnaire."
    )

    print("\n" + "=" * 72)
    print("FIN DU CALCUL")
    print("=" * 72)


if __name__ == "__main__":
    main()