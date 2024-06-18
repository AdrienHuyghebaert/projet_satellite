# ==========================================================================================
# Classe: AjoutOrbite
# Cette classe permet d'ajouter les paramètres d'orbite d'un satellite ou de modifier les
# paramètres d'un satellite déjà présent dans la base de données7
# Cette fonctionnalité est possible à partir du fichier YAML !
# ==========================================================================================

import pandas as pd
import numpy as np
import csv

class AjoutOrbite:
    def __init__(self, nom_fichier_csv, donnees, delimiter = ' '):
        self.nom_fichier_csv = nom_fichier_csv
        self.donnees = donnees
        self.delimiter = delimiter

    def ajouter_orbite(self):

        with open(self.nom_fichier_csv, mode='a', newline='') as file:
            # Créer un writer dico pour écrire les données
            writer = csv.DictWriter(file, fieldnames= self.donnees.keys(), delimiter=self.delimiter)

            # Ajouter la nouvelle ligne de données
            writer.writerow(self.donnees)

        print(f"Les nouvelles données ont été ajoutées au fichier {self.nom_fichier_csv}.")

