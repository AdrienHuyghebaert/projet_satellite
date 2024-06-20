import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from .affichage_terre import *

rayon_terre = 6371
centre_terre = np.array([0, 0, 0])


class AffichageOrbiteTraceConnection:

    def __init__(self, positions_satellites, nb_satellites, a_satellites, b_satellites):
        self.nb_points = 1000
        self.positions_satellites = np.array(positions_satellites)  # Convertir en tableau NumPy
        self.nb_satellites = nb_satellites
        self.a_satellites = a_satellites
        self.b_satellites = b_satellites
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.satellites = []
        self.connexion_line = None  # Attribut pour stocker la ligne de connexion

        # Décalage aléatoire des positions initiales des satellites
        for i in range(self.nb_satellites):
            decalage = np.random.randint(self.nb_points)
            # Décalage circulaire des positions avec np.roll (CHAT.GPT)
            self.positions_satellites[i] = np.roll(self.positions_satellites[i], -decalage, axis=1)
            # Plot initial du satellite à la nouvelle position décalée
            satellite, = self.ax.plot([self.positions_satellites[i, 0, -1]],
                                      [self.positions_satellites[i, 1, -1]],
                                      [self.positions_satellites[i, 2, -1]], 'ro',
                                      markersize=8)
            self.satellites.append(satellite)

        # Initialisation de la ligne de connexion entre le premier et le deuxième satellite
        self.tracer_droite_entre_satellites(0, 1)

    def afficher_terre(self):
        coord_terre_lon, coord_terre_lat = afficher_terre()
        for x, y, z in coord_terre_lon:
            self.ax.plot(x, y, z, '-k')
        for x, y, z in coord_terre_lat:
            self.ax.plot(x, y, z, '-k')

    def tracer_orbites(self):
        for i in range(self.nb_satellites):
            self.ax.plot(self.positions_satellites[i, 0], self.positions_satellites[i, 1],
                         self.positions_satellites[i, 2], 'b-', label='Orbite')

        # Configuration des limites des axes
        max_a = np.max(self.a_satellites)
        max_b = np.max(self.b_satellites)
        self.ax.set_xlim(-max_a - 1000, max_a + 1000)
        self.ax.set_ylim(-max_a - 1000, max_a + 1000)
        self.ax.set_zlim(-max_b - 1000, max_b + 1000)
        self.ax.set_aspect('auto')

    def tracer_droite_entre_satellites(self, satellite1_idx, satellite2_idx):
        x_coords = [self.positions_satellites[satellite1_idx, 0, -1], self.positions_satellites[satellite2_idx, 0, -1]]
        y_coords = [self.positions_satellites[satellite1_idx, 1, -1], self.positions_satellites[satellite2_idx, 1, -1]]
        z_coords = [self.positions_satellites[satellite1_idx, 2, -1], self.positions_satellites[satellite2_idx, 2, -1]]

        if self.connexion_line is None:
            self.connexion_line, = self.ax.plot(x_coords, y_coords, z_coords, 'g--', linewidth=2)
        else:
            self.connexion_line.set_data(x_coords, y_coords)
            self.connexion_line.set_3d_properties(z_coords)

    def initialiser_animation(self):
        for satellite in self.satellites:
            satellite.set_data([], [])
            satellite.set_3d_properties([])
        return self.satellites

    def update_animation(self, n):
        artists = []

        # Mise à jour des positions des satellites
        for i in range(self.nb_satellites):
            x = self.positions_satellites[i, 0, n]
            y = self.positions_satellites[i, 1, n]
            z = self.positions_satellites[i, 2, n]

            self.satellites[i].set_data([x], [y])
            self.satellites[i].set_3d_properties([z])
            artists.append(self.satellites[i])

        # Mettre à jour la ligne de connexion entre le premier et le deuxième satellite
        satellite1_idx = 0
        satellite2_idx = 1
        x_coords = [self.positions_satellites[satellite1_idx, 0, n], self.positions_satellites[satellite2_idx, 0, n]]
        y_coords = [self.positions_satellites[satellite1_idx, 1, n], self.positions_satellites[satellite2_idx, 1, n]]
        z_coords = [self.positions_satellites[satellite1_idx, 2, n], self.positions_satellites[satellite2_idx, 2, n]]

        if self.connexion_line is None:
            self.connexion_line, = self.ax.plot(x_coords, y_coords, z_coords, 'g-', linewidth=2)
        else:
            self.connexion_line.set_data(x_coords, y_coords)
            self.connexion_line.set_3d_properties(z_coords)

        artists.append(self.connexion_line)  # Ajouter la ligne de connexion aux artistes à redessiner

        return artists

    def animate(self):
        print(self.nb_satellites)
        self.tracer_orbites()
        self.afficher_terre()
        anim = animation.FuncAnimation(self.fig, self.update_animation, init_func=self.initialiser_animation,
                                       frames=self.nb_points, interval=20, blit=True)
        plt.show()
