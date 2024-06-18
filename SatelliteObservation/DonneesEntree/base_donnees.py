# ==========================================================================================
# Classe: BaseDonnees
# Cette classe permet de gérer la base de données des satellite et de chercher les informations d'un satellite
# par son numéro d'identification NORAD
# ==========================================================================================

import pandas as pd
import numpy as np

class BaseDonnees:

    def __init__(self, nom_base_donnee, NORAD_number):
        self.nom_base_donnee = nom_base_donnee
        self.NORAD_number = NORAD_number

    # Table utilisée: 'UCS-Satellite-Database 5-1-2023.csv'

    def lire_base_donnees(self):

        # Lecture du fichier .csv
        tableau = pd.read_csv(self.nom_base_donnee, delimiter=';', decimal=',', thousands=' ',
                         usecols=(1, 8, 10, 11, 12, 13, 14, 15, 16, 17, 25, 26))
        return tableau

    def traitement_base_donnees(self):

        df = self.lire_base_donnees()

        # print('Avant traitement, liste des colonnes retenues:\n')
        # print(df.columns)
        # print('\n')

        # Remplacer les cases vides par NaN
        df.replace(" ", np.nan, inplace=True)


        # Remplacer les ',' par des '.'
        df = df.apply(lambda x: x.str.replace(',', '.') if x.dtype == "object" else x)

        # Enlever les lignes avec des valeurs non connues NaN
        df = df.dropna()

        # Transformer les valeurs numériques en float
        for col in ['Perigee (km)','Apogee (km)','Eccentricity', 'Inclination (degrees)', 'Period (minutes)', 'Launch Mass (kg.)', 'Longitude of GEO (degrees)']:
            df[col] = df[col].astype(float)

        # Ne garder que les satellites en orbite basse LEO
        #df_LEO = df[df['Class of Orbit'] == 'LEO'].reset_index(drop=True)

        #print(df)
        # Récupérer les données de la table pour un satellite donné (1 ligne)
        return df

    def enregistrer_base_donnees(self):
        # Enregistrer le fichier .csv prêt à l'emploi
        df = self.lire_base_donnees()
        df.to_csv('Base_donnees_satellites.csv')

    def appel_base_donnees(self):
        base_donnees = self.traitement_base_donnees()

        # Trouver un satellite par son numéro
        numero_NORAD_sat = self.NORAD_number
        donnees_satellite = base_donnees.loc[base_donnees['NORAD Number'] == numero_NORAD_sat]
        return donnees_satellite



