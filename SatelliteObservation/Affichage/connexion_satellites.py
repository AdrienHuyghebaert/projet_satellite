import numpy as np
import matplotlib.pyplot as plt

centre_terre = np.zeros(3)
rayon_terre = 6371


class ConnexionSatellites:

    def __init__(self, binome, positions_satellites):
        self.positions_satellites = positions_satellites
        self.satellite_1 = binome[0]
        self.satellite_2 = binome[1]
        self.ligne = {}

    def tracer_connexion_entre_satellites(self):
        x_coords = [self.positions_satellites[self.satellite_1, 0, -1], self.positions_satellites[self.satellite_2, 0, -1]]
        y_coords = [self.positions_satellites[self.satellite_1, 1, -1], self.positions_satellites[self.satellite_2, 1, -1]]
        z_coords = [self.positions_satellites[self.satellite_1, 2, -1], self.positions_satellites[self.satellite_2, 2, -1]]

        # Création de la nouvelle ligne (ou MAJ) de la ligne dans le dictionnaire
        line = plt.plot(x_coords, y_coords, z_coords, 'g-', linewidth=2)
        self.ligne[(self.satellite_1, self.satellite_2)] = line
        return self.ligne[(self.satellite_1, self.satellite_2)]

    def tester_connexion_satellites(self, position_sat_1, position_sat_2):
        point_centre = centre_terre
        point_droite = np.array(position_sat_1)
        vect = np.array(position_sat_2 - position_sat_1)
        projection = point_droite + np.dot(point_centre - point_droite, vect) / np.dot(vect, vect) * vect
        distance = np.linalg.norm(projection - point_centre)
        return distance

    def mettre_a_jour_connexions(self, n):
        x_coords = [self.positions_satellites[self.satellite_1, 0, n],
                    self.positions_satellites[self.satellite_2, 0, n]]
        y_coords = [self.positions_satellites[self.satellite_1, 1, n],
                    self.positions_satellites[self.satellite_2, 1, n]]
        z_coords = [self.positions_satellites[self.satellite_1, 2, n],
                    self.positions_satellites[self.satellite_2, 2, n]]

        position_sat_1 = np.array([x_coords[0], y_coords[0], z_coords[0]])
        position_sat_2 = np.array([x_coords[1], y_coords[1], z_coords[1]])
        distance = self.tester_connexion_satellites(position_sat_1, position_sat_2)

        if distance > rayon_terre:
            self.ligne[(self.satellite_1, self.satellite_2)].line.set_data(x_coords, y_coords)
            self.ligne[(self.satellite_1, self.satellite_2)].line.set_3d_properties(z_coords)

        else:
            self.ligne[(self.satellite_1, self.satellite_2)].line.set_data([0, 0], [0, 0])
            self.ligne[(self.satellite_1, self.satellite_2)].line.set_3d_properties([0, 0])

        return self.ligne[(self.satellite_1, self.satellite_2)]
