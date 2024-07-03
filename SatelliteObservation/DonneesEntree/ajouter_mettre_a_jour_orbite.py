# ==============================================================================================================
# Auteurs: Groupe 5
# Classe: AjoutOrbite
# Fonction: Cette classe permet d'ajouter les paramètres d'orbite d'un satellite ou de modifier les
# paramètres d'un satellite déjà présent dans la base de données
# Cette fonctionnalité est possible à partir du fichier YAML et de la data frame créée à partir du fichier csv.
# ===============================================================================================================

import pandas as pd
import numpy as np
import os


class AjoutOrbite:
    def __init__(self, nom_base_donnees):
        self.nom_base_donnees = nom_base_donnees

    # Retourner la table panda avec les colonnes sélectionnées:=========================================================
    def lire_base_donnees(self):

        tableau = pd.read_csv(self.nom_base_donnees, delimiter=';', decimal=',', thousands=' ',
                              usecols=(1, 8, 9, 10, 11, 12, 13, 14, 15, 16, 26))

        # On renomme les colonnes de la table
        tableau.columns = ['Nom_Satellite', 'Classe_Orbite', 'Type_Orbite', 'Longitude (deg)',
                           'Perigee (km)', 'Apogee (km)', 'Excentricite', 'Inclinaison (deg)', 'Periode', 'Masse',
                           'Numero_NORAD']

        # Réordonner les colonnes
        ordre_colonnes = ['Apogee (km)', 'Perigee (km)', 'Inclinaison (deg)', 'Numero_NORAD', 'Masse', 'Periode',
                          'Excentricite',
                          'Nom_Satellite', 'Classe_Orbite', 'Type_Orbite', 'Longitude (deg)']

        tableau = tableau[ordre_colonnes]

        return tableau

    # Traite la base de données et la renvoie: =========================================================================
    def traitement_base_donnees(self):

        df = self.lire_base_donnees()
        # Remplacer les cases vides par NaN
        df.replace(" ", np.nan, inplace=True)

        # Remplacer les ',' par des '.'
        df = df.apply(lambda x: x.str.replace(',', '.') if x.dtype == "object" else x)

        # Enlever les lignes avec des valeurs non connues NaN
        df = df.dropna()

        # Transformer les valeurs numériques en float
        for col in ['Longitude (deg)', 'Perigee (km)', 'Apogee (km)', 'Excentricite', 'Inclinaison (deg)', 'Periode']:
            df[col] = df[col].astype(float)

        return df

    # Ajouter une nouvelle ligne dans la data frame et enregistre le fichier csv correspondant: ========================

    def ajouter_orbite(self, donnees, deja_modifie):

        if deja_modifie == True:

            data_frame = pd.read_csv(self.nom_base_donnees, delimiter=',', decimal='.', thousands=' ')

        elif deja_modifie == False:

            data_frame = self.traitement_base_donnees()

        new_data_frame = pd.concat([data_frame, pd.DataFrame(donnees.values(), columns=data_frame.columns)],
                                   ignore_index=True)

        # Enregistrer le DataFrame dans un fichier CSV
        nom_fichier_csv = 'Base_donnees_satellites_utilisateur.csv'

        # Le nouveau fichier csv est ajouter au dossier des données d'entrée
        dossier_destination = os.path.join('Entrees')

        nom_fichier_csv = os.path.join(dossier_destination, nom_fichier_csv)

        new_data_frame.to_csv(nom_fichier_csv, index=False)
        return new_data_frame

    # Modifie une donnée d'une orbite existante dans la data frame et enregistre le fichier csv: =======================
    def modifier_orbite(self, nom_colonne, numero_NORAD, valeur_modifiee, deja_modifie):

        if deja_modifie == True:

            df = pd.read_csv(self.nom_base_donnees, delimiter=',', decimal='.', thousands=' ')


        elif deja_modifie == False:

            df = self.traitement_base_donnees()

        df.loc[df['Numero_NORAD'] == numero_NORAD, nom_colonne] = valeur_modifiee


        nom_fichier_csv = 'Base_donnees_satellites_utilisateur.csv'

        # Le nouveau fichier csv est ajouté au dossier des données d'entrée et est enregistré

        dossier_destination = os.path.join('Entrees')

        nom_fichier_csv = os.path.join(dossier_destination, nom_fichier_csv)

        df.to_csv(nom_fichier_csv, index=False)

        return df
