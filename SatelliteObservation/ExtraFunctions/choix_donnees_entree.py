# ======================================================================================================================
# Auteurs: Groupe 5
# Date: 02/07/2024
# Fonction: Ce programme permet de sélectionner les données d'entrée selon le choix de l'utilisateur et de les
# renvoyer sous format de tableau numpy pour leur utilisation dans affichage
# ======================================================================================================================

import SatelliteObservation
import numpy as np
import pandas as pd


def choisir_format_entree(choix_donnees, nombre_satellite):
    # Entrée: fichier YAML
    if choix_donnees == 1:
        print('\n Veuillez renseigner les données dans le fichier deck.yaml avant de poursuivre')
        choix_yaml = (SatelliteObservation.get_int_input
                      ('\n \u21D2 Voulez-vous utiliser les données satellite (tapez 0)'
                       ' ou bien les données TLE (tapez 1): \n'))

        # Entrée YAML: données satellite
        if choix_yaml == 0:
            tableau = np.zeros((nombre_satellite, 11), dtype=object)
            for i in range(nombre_satellite):

                # Vérifier si l'utilisateur a déjà modifié le fichier deck.yaml pour le satellite
                reponse = input(
                    f"Avez-vous déjà modifié le fichier deck.yaml pour le satellite {i + 1} ? (oui/non): ").lower()

                if reponse == 'oui':
                    fichier_yaml = SatelliteObservation.Lire_YAML('Entrees/deck.yaml')  # instanciation objet classe
                    donnees_sat = fichier_yaml.donnees_satellite()[1]
                    donnees_orb = fichier_yaml.donnees_satellite()[0]
                    concat_dict = {**donnees_orb, **donnees_sat}

                else:
                    input("Appuyez sur Entrée lorsque vous avez terminé de modifier le fichier...")

                    # Réinstancer l'objet après modification
                    fichier_yaml = SatelliteObservation.Lire_YAML('Entrees/deck.yaml')  # instanciation objet class
                    donnees_sat = fichier_yaml.donnees_satellite()[1]
                    donnees_orb = fichier_yaml.donnees_satellite()[0]
                    concat_dict = {**donnees_orb, **donnees_sat}

                # Permet de mettre le numéro NORAD  à l'endroit voulu dans la liste
                liste = list(concat_dict.values())
                numero_norad = liste.pop(9)
                liste.insert(3, numero_norad)

                numerical_cols = [0, 1, 2, 3, 6, 7, 8, 10]  # Indices des colonnes numériques (float) dans le tableau

                # # Modifications du type des données numériques de string à float dans un tableau numpy
                for col_idx in range(11):
                    if col_idx in numerical_cols:
                        tableau[i][col_idx] = float(liste[col_idx])

                    else:
                        tableau[i][col_idx] = liste[col_idx]

        # Entrée YAML: TLE
        elif choix_donnees == 1:

            tableau = np.zeros((nombre_satellite, 7), dtype=object)

            for i in range(nombre_satellite):

                # Vérifier si l'utilisateur a déjà modifié le fichier deck.yaml pour le satellite
                reponse = input(
                    f"Avez-vous déjà modifié le fichier deck.yaml pour le satellite {i + 1} ? (oui/non): ").lower()

                if reponse == 'oui':
                    fichier_yaml_TLE = SatelliteObservation.Lire_YAML('Entrees/deck.yaml')  # Instanciation de l'objet
                    donnees = fichier_yaml_TLE.donnees_TLE()

                else:
                    input("Appuyez sur Entrée lorsque vous avez terminé de modifier le fichier...")

                    # Réinstancer l'objet de la classe après modification

                    fichier_yaml_TLE = SatelliteObservation.Lire_YAML('Entrees/deck.yaml')
                    donnees = fichier_yaml_TLE.donnees_TLE()

                tableau[i] = donnees

                numerical_cols = [0, 1, 2, 3, 5, 6]  # Indices des colonnes numériques (float) dans le tableau

                # Modifications du type des données numériques de string à float dans un tableau numpy
                for col_idx in range(7):
                    if col_idx in numerical_cols:
                        tableau[i][col_idx] = float(tableau[i][col_idx])

                    else:
                        tableau[i][col_idx] = tableau[i][col_idx]

    # Entrée: Base de données (fichier csv)
    elif choix_donnees == 2:

        tableau = np.zeros((nombre_satellite, 11), dtype=object)

        for i in range(nombre_satellite):
            while True:
                numero_NORAD = SatelliteObservation.get_int_input(
                    'Entrez le numéro NORAD du satellite à étudier (5 chiffres):')

                base = SatelliteObservation.BaseDonnees('Entrees/UCS-Satellite-Database 5-1-2023.csv', numero_NORAD)
                base_donnees = base.appel_base_donnees()[1]

                # Conversion de la ligne de donnée de la data frame en tableau numpy si le numéro NORAD existe
                if numero_NORAD in base_donnees['Numero_NORAD'].values:
                    valeurs_ligne = base.appel_base_donnees()[0]
                    ligne = valeurs_ligne.values.tolist()[0]
                    break

                else:
                    print("Ce numéro n'existe pas dans la base de données veuillez réessayer !")

            # Transformation des données numériques de la table en float

            numerical_cols = [0, 1, 2, 3, 4, 5, 6, 10]  # Indices des colonnes numériques dans le tableau

            for col_idx in range(11):
                if col_idx in numerical_cols:
                    tableau[i][col_idx] = float(ligne[col_idx])

                else:
                    tableau[i][col_idx] = ligne[col_idx]

    # Affichage console en table panda pour plus de lisibilité:

    pd.set_option('display.max_rows', None)  # None pour afficher toutes les lignes
    pd.set_option('display.max_columns', None)  # None pour afficher toutes les colonnes

    index = [f'Satellite {i + 1}' for i in range(nombre_satellite)]

    columns = ['Apogee (km)', 'Perigee (km)', 'Inclinaison (deg)', 'Numero_NORAD', 'Masse', 'Periode', 'Excentricite',
               'Nom_Satellite', 'Classe_Orbite', 'Type_Orbite', 'Longitude (deg)']

    df = pd.DataFrame(tableau, columns=columns, index=index)

    print('\n', '=' * 150, '\n', '\nVoici les données du/des satellite(s) sélectionné(s): \n\n', df, '\n', '=' * 150)

    return tableau
