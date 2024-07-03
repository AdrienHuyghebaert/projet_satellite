# ====================================================================================================================
# Auteurs: Groupe 5
# Classe: BaseDonnees
# Date : 02/07/24
# Fonction: Cette classe permet de gérer la base de données des satellite et de chercher les informations d'un satellite
# par son numéro d'identification NORAD
# ======================================================================================================================

import pandas as pd
import numpy as np

import SatelliteObservation

class BaseDonnees:

    def __init__(self, nom_base_donnees, NORAD_number):
        self.nom_base_donnees = nom_base_donnees
        self.NORAD_number = NORAD_number

    # Table utilisée: 'UCS-Satellite-Database 5-1-2023.csv'

# Retourner la table panda avec les colonnes sélectionnées:=============================================================

    def lire_base_donnees(self):

        tableau = pd.read_csv(self.nom_base_donnees, delimiter=';', decimal=',', thousands=' ',
                              usecols=(1, 8, 9, 10, 11, 12, 13, 14, 15, 16, 26))

        # On renomme les colonnes de la table
        tableau.columns = ['Nom_Satellite', 'Classe_Orbite', 'Type_Orbite', 'Longitude (deg)',
                           'Perigee (km)', 'Apogee (km)', 'Excentricite', 'Inclinaison (deg)', 'Periode', 'Masse',
                           'Numero_NORAD']

        # Réordonner les colonnes
        ordre_colonnes = ['Apogee (km)', 'Perigee (km)', 'Inclinaison (deg)', 'Numero_NORAD', 'Masse', 'Periode',
                          'Excentricite', 'Nom_Satellite', 'Classe_Orbite', 'Type_Orbite', 'Longitude (deg)']

        tableau = tableau[ordre_colonnes]

        return tableau

# Traite la base de données et la renvoie: =============================================================================
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

# Enregistre la nouvelle base de donnée sous un fichier csv: ===========================================================
    def enregistrer_base_donnees(self):
        # Enregistrer le fichier .csv prêt à l'emploi
        df = self.lire_base_donnees()
        df.to_csv('Base_donnees_satellites.csv')

# Renvoie les données d'un satellite trouvé dans la base de données sous son numéro NORAD: =============================
    def appel_base_donnees(self):
        base_donnees = self.traitement_base_donnees()

        # Trouver un satellite par son numéro
        numero_NORAD_sat = self.NORAD_number

        donnees_satellite = base_donnees.loc[base_donnees['Numero_NORAD'] == numero_NORAD_sat]

        return donnees_satellite, base_donnees
