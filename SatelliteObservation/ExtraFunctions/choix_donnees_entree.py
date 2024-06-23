# ======================================================================================================================
# Auteurs: Groupe
# Date: 20/06/2024
# Programme: Ce programme permet de sélectionner les données d'entrée selon le choix de l'utilisateur
# ======================================================================================================================

import SatelliteObservation
import numpy as np
import pandas as pd

def choisir_format_entree(choix_donnees, nombre_satellite):

    tableau = np.empty((nombre_satellite,), dtype=object)

# Entrée: fichier YAML
    if choix_donnees == 1:
        print('\n Veuillez renseigner les données dans le fichier deck.yaml avant de poursuivre')
        choix_yaml = (SatelliteObservation.get_int_input
                         ('\n \u21D2 Voulez-vous utiliser les données satellite (tapez 0) ou bien les données TLE (tapez 1): \n'))

        # Entrée YAML: données satellite
        if choix_yaml == 0:
            for i in range(nombre_satellite):

                # Vérifier si l'utilisateur a déjà modifié le fichier deck.yaml pour le satellite
                reponse = input(
                    f"Avez-vous déjà modifié le fichier deck.yaml pour le satellite {i + 1} ? (oui/non): ").lower()

                if reponse == 'oui':
                    fichier_yaml = SatelliteObservation.Lire_YAML('Entrees/deck.yaml') # instanciation objet
                    donnees_sat = fichier_yaml.donnees_satellite()[1]
                    donnees_orb = fichier_yaml.donnees_satellite()[0]

                else:
                    input("Appuyez sur Entrée lorsque vous avez terminé de modifier le fichier...")


                    # Réinstancer l'objet après modification
                    fichier_yaml = SatelliteObservation.Lire_YAML('Entrees/deck.yaml')  # instanciation objet
                    donnees_sat = fichier_yaml.donnees_satellite()[1]
                    donnees_orb = fichier_yaml.donnees_satellite()[0]

                tableau[i] = np.array(list(donnees_orb.values()))



        # Entrée YAML: TLE
        elif choix_donnees == 1:
            compteur = nombre_satellite
            for i in range(nombre_satellite):

                # Vérifier si l'utilisateur a déjà modifié le fichier deck.yaml pour le satellite
                reponse = input(
                    f"Avez-vous déjà modifié le fichier deck.yaml pour le satellite {i + 1} ? (oui/non): ").lower()
                if reponse == 'oui':
                    fichier_yaml_TLE = SatelliteObservation.Lire_YAML('Entrees/deck.yaml')  # Instanciation de l'objet
                    donnees = fichier_yaml_TLE.donnees_TLE()
                else:
                    input("Appuyez sur Entrée lorsque vous avez terminé de modifier le fichier...")

                    # Réinstancer l'objet après modification
                    fichier_yaml_TLE = SatelliteObservation.Lire_YAML('Entrees/deck.yaml')
                    donnees = fichier_yaml_TLE.donnees_TLE()

                tableau[i] = donnees


    # Entrée: Base de données (fichier csv)
    elif choix_donnees == 2:
        for i in range(nombre_satellite):
            numero_NORAD = SatelliteObservation.get_int_input('Entrez le numéro NORAD du satellite à étudier (5 chiffres):')
            base = SatelliteObservation.BaseDonnees('Entrees/UCS-Satellite-Database 5-1-2023.csv', numero_NORAD)

            # Conversion de la ligne de donnée de la data frame en tableau numpy
            valeurs_ligne = base.appel_base_donnees()
            tableau[i] = valeurs_ligne.to_numpy()

    # Affichage console:

    pd.set_option('display.max_rows', None)  # None pour afficher toutes les lignes
    pd.set_option('display.max_columns', None)  # None pour afficher toutes les colonnes

    index = [f'Satellite {i + 1}' for i in range(nombre_satellite)]

    df = pd.DataFrame(tableau, columns=['Données des satellites'], index =index)

    print('\nVoici les données du/des satellite(s) sélectionné(s): \n\n', df)

    return tableau

