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

    def initialiser_animation(self):
        for satellite in self.satellites:
            satellite.set_data([], [])
            satellite.set_3d_properties([])
        return self.satellites

    def update_animation(self, n):
        artists = []
        for i in range(self.nb_satellites):
            x = self.positions_satellites[i, 0, n]
            y = self.positions_satellites[i, 1, n]
            z = self.positions_satellites[i, 2, n]
            self.satellites[i].set_data([x], [y])
            self.satellites[i].set_3d_properties([z])
            artists.append(self.satellites[i])
        return artists

    def animate(self):
        print(self.nb_satellites)
        self.tracer_orbites()
        self.afficher_terre()
        anim = animation.FuncAnimation(self.fig, self.update_animation, init_func=self.initialiser_animation,
                                       frames=self.nb_points, interval=20, blit=True)
        plt.show()
