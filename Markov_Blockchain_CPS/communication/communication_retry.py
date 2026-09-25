"""
Modèle DTMC simplifié — Communication PLC -> Edge -> Blockchain.

Une tentative de transmission réussit avec une probabilité de 0.90.
Une retransmission est effectuée en cas d'échec, avec au maximum
3 tentatives.

Objectifs :
    - probabilité de succès après 1 tentative ;
    - probabilité de succès après 2 tentatives ;
    - probabilité de succès après 3 tentatives ;
    - probabilité d'abandon après 3 échecs.
"""

SUCCESS_PROBABILITY = 0.90
FAILURE_PROBABILITY = 1 - SUCCESS_PROBABILITY
MAX_ATTEMPTS = 3


def success_probability(attempts):
    """
    Probabilité d'obtenir au moins un succès en 'attempts' tentatives.
    """
    return 1 - (FAILURE_PROBABILITY ** attempts)


def failure_probability(attempts):
    """
    Probabilité d'échouer à toutes les tentatives.
    """
    return FAILURE_PROBABILITY ** attempts


def main():

    print("=" * 70)
    print("COMMUNICATION PLC -> EDGE -> BLOCKCHAIN")
    print("=" * 70)

    print("\nParamètres du modèle")
    print("-" * 70)
    print(f"Probabilité de succès par tentative : "
          f"{SUCCESS_PROBABILITY * 100:.2f} %")
    print(f"Probabilité d'échec par tentative   : "
          f"{FAILURE_PROBABILITY * 100:.2f} %")
    print(f"Nombre maximal de tentatives        : {MAX_ATTEMPTS}")

    print("\nPROBABILITÉS DE SUCCÈS AVEC RETRANSMISSION")
    print("-" * 70)

    for attempts in range(1, MAX_ATTEMPTS + 1):

        success = success_probability(attempts)
        failure = failure_probability(attempts)

        print(
            f"{attempts} tentative(s) : "
            f"succès = {success * 100:6.2f} % | "
            f"échec final = {failure * 100:6.2f} %"
        )

    # Résultat final après 3 tentatives
    final_success = success_probability(MAX_ATTEMPTS)
    final_failure = failure_probability(MAX_ATTEMPTS)

    print("\nRÉSULTAT FINAL")
    print("-" * 70)

    print(
        f"Probabilité de succès après {MAX_ATTEMPTS} tentatives : "
        f"{final_success * 100:.2f} %"
    )

    print(
        f"Probabilité d'abandon après {MAX_ATTEMPTS} échecs : "
        f"{final_failure * 100:.2f} %"
    )

    improvement = final_success / SUCCESS_PROBABILITY

    print(
        f"\nGain relatif par rapport à une seule tentative : "
        f"{improvement:.2f} fois"
    )

    print("\nINTERPRÉTATION")
    print("-" * 70)

    print(
        "Sans retransmission, une tentative présente 90 % de "
        "probabilité de succès."
    )

    print(
        "Avec trois tentatives indépendantes, la probabilité "
        "d'obtenir au moins un succès atteint 99.90 %."
    )

    print(
        "La probabilité d'échec complet est alors réduite à 0.10 %."
    )

    print("\n" + "=" * 70)
    print("FIN DU CALCUL")
    print("=" * 70)


if __name__ == "__main__":
    main()