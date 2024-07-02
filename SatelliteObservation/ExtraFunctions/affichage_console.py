# ======================================================================================================================
# Auteurs: Groupe 5
# Date: 20/06/2024
# Programme: Ce programme permet d'afficher les messsages console pour l'utilisateur
# ======================================================================================================================

import SatelliteObservation


def afficher_console(titre):

    longueur = len(titre) + 4
    print("=" * longueur)
    print(f"| {titre} |")
    print("=" * longueur, '\n')
