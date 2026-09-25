"""
Analyse de sensibilité — Modèle Blockchain-CPS/PLC.

Cette analyse étudie l'influence de plusieurs paramètres
sur le comportement probabiliste du système :

1. MTTR : 1 h -> 4 h
2. Taux de panne directe : 0.005 -> 0.040 / h
3. Détection Normal -> Suspect : 0.01 -> 0.10
4. Transition Suspect -> Compromis : 0.10 -> 0.70

Les paramètres de référence correspondent au cahier des charges.
"""

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. DISPONIBILITÉ — INFLUENCE DU MTTR
# ============================================================

def stationary_distribution(Q):
    """
    Calcule pi tel que pi Q = 0 et somme(pi) = 1.
    """

    A = Q.T.copy()
    A[-1, :] = 1.0

    b = np.zeros(len(Q))
    b[-1] = 1.0

    return np.linalg.solve(A, b)


def availability_from_mttr(mttr):
    """
    Modèle CTMC de disponibilité.

    États :
        Disponible
        Dégradé
        Indisponible

    Le taux de réparation est :
        mu = 1 / MTTR
    """

    repair_rate = 1.0 / mttr

    Q = np.array([
        [-0.06, 0.05, 0.01],
        [0.20, -0.25, 0.05],
        [repair_rate, 0.00, -repair_rate]
    ])

    pi = stationary_distribution(Q)

    return pi


def analyze_mttr():

    mttr_values = np.array([
        1.0,
        1.5,
        2.0,
        2.5,
        3.0,
        3.5,
        4.0
    ])

    availability = []

    for mttr in mttr_values:

        pi = availability_from_mttr(mttr)

        availability.append(
            pi[0] * 100
        )

    print("\n" + "=" * 72)
    print("SENSIBILITÉ — INFLUENCE DU MTTR")
    print("=" * 72)

    print(
        f"{'MTTR (h)':<15}"
        f"{'Disponible':>20}"
    )

    for mttr, value in zip(
        mttr_values,
        availability
    ):

        print(
            f"{mttr:<15.1f}"
            f"{value:>18.2f} %"
        )

    plt.figure(figsize=(8, 5))

    plt.plot(
        mttr_values,
        availability,
        marker="o"
    )

    plt.xlabel("MTTR (heures)")
    plt.ylabel("Disponibilité stationnaire (%)")
    plt.title("Influence du MTTR sur la disponibilité")
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "sensitivity_mttr.png",
        dpi=300
    )

    plt.show()


# ============================================================
# 2. DISPONIBILITÉ — TAUX DE PANNE DIRECTE
# ============================================================

def availability_from_failure_rate(failure_rate):

    degradation_rate = 0.05
    repair_rate = 0.50

    # Le taux de sortie de Disponible est :
    # dégradation + panne directe
    total_failure_rate = (
        degradation_rate + failure_rate
    )

    Q = np.array([
        [-total_failure_rate,
         degradation_rate,
         failure_rate],

        [0.20,
         -0.25,
         0.05],

        [repair_rate,
         0.00,
         -repair_rate]
    ])

    pi = stationary_distribution(Q)

    return pi


def analyze_failure_rate():

    rates = np.array([
        0.005,
        0.010,
        0.015,
        0.020,
        0.025,
        0.030,
        0.035,
        0.040
    ])

    availability = []

    for rate in rates:

        pi = availability_from_failure_rate(rate)

        availability.append(
            pi[0] * 100
        )

    print("\n" + "=" * 72)
    print("SENSIBILITÉ — TAUX DE PANNE DIRECTE")
    print("=" * 72)

    print(
        f"{'Taux panne (/h)':<20}"
        f"{'Disponible':>20}"
    )

    for rate, value in zip(
        rates,
        availability
    ):

        print(
            f"{rate:<20.3f}"
            f"{value:>18.2f} %"
        )

    plt.figure(figsize=(8, 5))

    plt.plot(
        rates,
        availability,
        marker="o"
    )

    plt.xlabel("Taux de panne directe (/heure)")
    plt.ylabel("Disponibilité stationnaire (%)")
    plt.title("Influence du taux de panne sur la disponibilité")
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "sensitivity_failure_rate.png",
        dpi=300
    )

    plt.show()


# ============================================================
# 3. CYBERSÉCURITÉ — NORMAL -> SUSPECT
# ============================================================

def cybersecurity_distribution(
    normal_to_suspect=0.03,
    suspect_to_compromised=0.30
):

    # Normal -> Normal
    normal_to_normal = (
        1 - normal_to_suspect
    )

    # Suspect -> Normal
    suspect_to_normal = 0.60

    # Suspect -> Suspect
    suspect_to_suspect = (
        1
        - suspect_to_normal
        - suspect_to_compromised
    )

    # Compromis
    compromised_to_compromised = 0.20
    compromised_to_isolated = 0.80

    # Isolé
    isolated_to_normal = 0.70
    isolated_to_isolated = 0.30

    P = np.array([

        [
            normal_to_normal,
            normal_to_suspect,
            0.00,
            0.00
        ],

        [
            suspect_to_normal,
            suspect_to_suspect,
            suspect_to_compromised,
            0.00
        ],

        [
            0.00,
            0.00,
            compromised_to_compromised,
            compromised_to_isolated
        ],

        [
            isolated_to_normal,
            0.00,
            0.00,
            isolated_to_isolated
        ]

    ])

    # Distribution stationnaire
    A = P.T - np.eye(4)

    A[-1, :] = 1.0

    b = np.zeros(4)
    b[-1] = 1.0

    pi = np.linalg.solve(A, b)

    return pi


def analyze_detection_probability():

    values = np.array([
        0.01,
        0.02,
        0.03,
        0.04,
        0.05,
        0.06,
        0.07,
        0.08,
        0.09,
        0.10
    ])

    compromised = []

    for value in values:

        pi = cybersecurity_distribution(
            normal_to_suspect=value
        )

        compromised.append(
            pi[2] * 100
        )

    print("\n" + "=" * 72)
    print("SENSIBILITÉ — NORMAL -> SUSPECT")
    print("=" * 72)

    print(
        f"{'P(Normal->Suspect)':<25}"
        f"{'Compromis':>20}"
    )

    for value, probability in zip(
        values,
        compromised
    ):

        print(
            f"{value:<25.2f}"
            f"{probability:>18.2f} %"
        )

    plt.figure(figsize=(8, 5))

    plt.plot(
        values,
        compromised,
        marker="o"
    )

    plt.xlabel("P(Normal → Suspect)")
    plt.ylabel("Probabilité stationnaire de Compromis (%)")
    plt.title("Influence de la détection sur la compromission")
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "sensitivity_detection.png",
        dpi=300
    )

    plt.show()


# ============================================================
# 4. CYBERSÉCURITÉ — SUSPECT -> COMPROMIS
# ============================================================

def analyze_compromise_probability():

    values = np.array([
        0.10,
        0.20,
        0.30,
        0.40,
        0.50,
        0.60,
        0.70
    ])

    compromised = []

    for value in values:

        pi = cybersecurity_distribution(
            normal_to_suspect=0.03,
            suspect_to_compromised=value
        )

        compromised.append(
            pi[2] * 100
        )

    print("\n" + "=" * 72)
    print("SENSIBILITÉ — SUSPECT -> COMPROMIS")
    print("=" * 72)

    print(
        f"{'P(Suspect->Compromis)':<27}"
        f"{'Compromis':>20}"
    )

    for value, probability in zip(
        values,
        compromised
    ):

        print(
            f"{value:<27.2f}"
            f"{probability:>18.2f} %"
        )

    plt.figure(figsize=(8, 5))

    plt.plot(
        values,
        compromised,
        marker="o"
    )

    plt.xlabel("P(Suspect → Compromis)")
    plt.ylabel("Probabilité stationnaire de Compromis (%)")
    plt.title("Influence du risque de compromission")
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "sensitivity_compromise.png",
        dpi=300
    )

    plt.show()


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("#" * 72)
    print("ANALYSE DE SENSIBILITÉ")
    print("Blockchain — CPS/PLC — Markov")
    print("#" * 72)

    analyze_mttr()

    analyze_failure_rate()

    analyze_detection_probability()

    analyze_compromise_probability()

    print("\n" + "#" * 72)
    print("ANALYSE DE SENSIBILITÉ TERMINÉE")
    print("#" * 72)