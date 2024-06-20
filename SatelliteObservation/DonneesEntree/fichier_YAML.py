# ==========================================================================================
# Classe: Lire_YAML
# Cette classe permet de récupérer les données d'entrées du fichier YAML deck.yaml
# ==========================================================================================

import math
import numpy as np

masse_terre = 5.974 * (10 ** 24)  # Masse de la Terre en kg
G = 6.67 * 10 ** (-11)  # Constante gravitationnelle universelle


class Lire_YAML:
    def __init__(self, nom_fichier):
        self.nom_fichier = nom_fichier

# Lit le fichier deck.yaml: ============================================================================================
    def lecture_fichier(self):
        # Récupération des données du YAML
        from SatelliteObservation.DonneesEntree.LecteurYAML import LecteurYAML
        # On crée un objet YAML au sein duquel on charge une instance de LecteurYAML qui lit le fichier "deck.yamL"
        parser = LecteurYAML(self.nom_fichier)
        # On exécute la fonction read_yaml() de notre objet LecteurYAML
        parsed_data = parser.read_yaml()
        # On imprime le contenu qui a été lu
        # print("Données brutes\n:" + str(parsed_data) + "\n")
        # print("Types des données lues:\n" + str(type(parsed_data)) + "\n")

        # print("Voici les données entrées dans le fichier YAML:")
        # for key, value in parsed_data.items():
        #     print(f"- {key}: {value}")
        #
        # print("\nLes formats sont reconnus:")
        # for key, value in parsed_data.items():
        #     print(f"- {value} est de type {type(value)}")
        return parsed_data

# Récupère les données du YAML sous forme de dictionnaire: =============================================================
    def donnees_satellite(self):
        parsed_data = self.lecture_fichier()

        # Création de tableaux de variables d'entrées:
        donnees_satellite = parsed_data["Satellite"]
        donnes_orbite = parsed_data["Orbite"]
        return donnes_orbite, donnees_satellite

# Récupère les données TLE du YAML: ====================================================================================
    def donnees_TLE(self):

        # Récupération des données

        parsed_data = self.lecture_fichier()
        ligne_1 = parsed_data["TLE_ligne1"].split()
        ligne_2 = parsed_data["TLE_ligne2"].split()
        numero_sat = int(ligne_1[1][:-1])
        classe_sat = str(ligne_1[1][-1])
        inclinaison = float(ligne_2[2])
        nbr_revolution = float(ligne_2[7])
        # Traitement de la donnée d'excentricite
        e_brut = float(ligne_2[4])
        nombre_caracteres = len(str(e_brut))
        excentricite = e_brut * (10**(-(nombre_caracteres+1)))

        # Calcul des paramètres à partir des données TLE

        periode = (1440 / nbr_revolution) * 60  # période orbitale en s
        mu = G * masse_terre  # on fait l'hypothèse que masse satellite << masse terre
        a = (mu * (periode / (2 * math.pi)) ** 2) ** (1 / 3)  # calcul du demi grand axe en km
        r_p = a * (1 - excentricite)  # rayon périgée en km
        r_a = a * (1 + excentricite)  # rayon apogée en km

        # Création de tableaux de variables d'entrées:
        donnees_satellite_orbite_TLE = np.array([numero_sat, classe_sat, a, excentricite, r_p, r_a, inclinaison])

        return donnees_satellite_orbite_TLE