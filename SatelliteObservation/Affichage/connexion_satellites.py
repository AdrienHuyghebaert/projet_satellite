# ==========================================================================================
# Classe: Connexion_Satellites
# Cette classe permet de créer des objets connexion_satellites qui permettent de représenter
# la capacité de 2 satellites a communiquer entre eux et d'en créer une ligne 3D
# ==========================================================================================

import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3D

centre_terre = np.zeros(3)
rayon_terre = 6371


class ConnexionSatellites:

    def __init__(self, binome, positions_sat_1, positions_sat_2):
        self.line = None
        self.sat_1 = binome[0]
        self.sat_2 = binome[1]
        self.positions_sat_1 = positions_sat_1
        self.positions_sat_2 = positions_sat_2

    def tracer_connexion_entre_satellites(self, ax, n):
        x_coords = [self.positions_sat_1[0, n],
                    self.positions_sat_2[0, n]]
        y_coords = [self.positions_sat_1[1, n],
                    self.positions_sat_2[1, n]]
        z_coords = [self.positions_sat_1[2, n],
                    self.positions_sat_2[2, n]]

        if self.line is None:  # Créer la ligne la première fois
            self.line = Line3D(x_coords, y_coords, z_coords, color='g', linewidth=2)
            ax.add_line(self.line)
        else:  # Mettre à jour la ligne
            position_sat_1 = np.array([x_coords[0], y_coords[0], z_coords[0]])
            position_sat_2 = np.array([x_coords[1], y_coords[1], z_coords[1]])
            distance = self.tester_connexion_satellites(position_sat_1, position_sat_2)

            if distance > rayon_terre:
                self.line.set_data_3d(x_coords, y_coords, z_coords)
            else:
                self.line.set_data_3d([0, 0], [0, 0], [0, 0])

        return self.line

    def tester_connexion_satellites(self, position_sat_1, position_sat_2):
        point_centre = centre_terre
        point_droite = np.array(position_sat_1)
        vect = np.array(position_sat_2 - position_sat_1)
        projection = point_droite + np.dot(point_centre - point_droite, vect) / np.dot(vect, vect) * vect
        distance = np.linalg.norm(projection - point_centre)
        return distance
