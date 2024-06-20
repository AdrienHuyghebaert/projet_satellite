# ==============================================================================================================
# Classe: AjoutOrbite
# Cette classe permet d'ajouter les paramètres d'orbite d'un satellite ou de modifier les
# paramètres d'un satellite déjà présent dans la base de données
# Cette fonctionnalité est possible à partir du fichier YAML et de la data frame créée à partir du fichier csv.
# ===============================================================================================================

import pandas as pd
import numpy as np
import os


class AjoutOrbite:
    def __init__(self, nom_base_donnees):
        self.nom_base_donnees = nom_base_donnees


# Retourner la table panda avec les colonnes sélectionnées:=============================================================
    def lire_base_donnees(self):

        # Lecture du fichier .csv
        tableau = pd.read_csv(self.nom_base_donnees, delimiter=';', decimal=',', thousands=' ',
                              usecols=(1, 8, 9, 10, 12, 13, 14, 15, 16, 17, 26))

        # On renomme les colonnes de la table
        tableau.columns = ['Nom_Satellite', 'Classe_Orbite', 'Type_Orbite', 'Longitude (deg)',
                           'Perigee (km)', 'Apogee (km)', 'Excentricite', 'Inclinaison (deg)', 'Periode',
                           'Masse', 'Numero_NORAD']
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

        # Ne garder que les satellites en orbite basse LEO
        # df_LEO = df[df['Class of Orbit'] == 'LEO'].reset_index(drop=True)

        return df

# Ajouter une nouvelle ligne dans la data frame: =======================================================================

    def ajouter_orbite(self, donnees):
        data_frame = self.traitement_base_donnees()
        new_data_frame = pd.concat([data_frame, pd.DataFrame(donnees.values(), columns=data_frame.columns)],
                                   ignore_index=True)
        return new_data_frame

# Modifie une donnée d'une orbite existante dans la data frame : =======================================================================
    def modifier_orbite(self, nom_colonne, numero_NORAD, valeur_modifiee):
        df= self.traitement_base_donnees()
        df.loc[df['Numero_NORAD'] == numero_NORAD, nom_colonne] = valeur_modifiee
        return df



# Enregistre la nouvelle base de donnée sous un fichier csv: ===========================================================
    def enregistrer_nouvelle_base_donnees(self):
        # Enregistrer le DataFrame dans un fichier CSV
        nom_fichier_csv = 'Base_donnees_satellites_ajout.csv'

        # Le nouveau fichier csv est ajouter au dossier des données d'entrée
        dossier_destination = os.path.join('Entrees')
        df = self.ajouter_orbite()
        nom_fichier_csv = os.path.join(dossier_destination, nom_fichier_csv)
        df.to_csv(nom_fichier_csv, index=False)

