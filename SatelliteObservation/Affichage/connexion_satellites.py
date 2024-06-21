import numpy as np

centre_terre = np.zeros(3)


class AffichageConnectionSatellites:

    def __init__(self, positions_satellites):

        self.positions_satellites = positions_satellites
        self.binomes_satellites = []  # Liste des connexions entre les satellites
        self.lignes_connexion = {}  # Dictionnaire pour stocker les lignes de connexion

    def initialisation_connexions(self):
        # Éviter les connexions doubles et les auto-connexions
        for i in range(len(self.positions_satellites)):
            for j in range(i + 1, len(self.positions_satellites)):
                self.binomes_satellites.append((i, j))  # Ajouter chaque couple unique de satellites
                self.connexion_entre_satellites(i, j)  # Créer la ligne initiale entre les 2 satellites

    def connexion_entre_satellites(self, satellite1_idx, satellite2_idx):
        x_coords = [self.positions_satellites[satellite1_idx, 0, -1], self.positions_satellites[satellite2_idx, 0, -1]]
        y_coords = [self.positions_satellites[satellite1_idx, 1, -1], self.positions_satellites[satellite2_idx, 1, -1]]
        z_coords = [self.positions_satellites[satellite1_idx, 2, -1], self.positions_satellites[satellite2_idx, 2, -1]]

        return x_coords, y_coords, z_coords

    def tester_connexion_satellites(self, position_sat_1, position_sat_2):
        # On définit le centre de la Terre à projeter sur la droite de connection entre les satellites
        point_centre = centre_terre
        point_droite = np.array(position_sat_1)

        # On définit la droite de connection entre les satellites
        vect = np.array(position_sat_2 - position_sat_1)

        # On projette le point sur la droite et on récupère ses coordonnées
        projection = point_droite + np.dot(point_centre - point_droite, vect) / np.dot(vect, vect) * vect

        # On calcule la distance entre le centre et le point projette
        distance = np.linalg.norm(projection - point_centre)

        return distance

    # def mettre_a_jour_connexions(self):
