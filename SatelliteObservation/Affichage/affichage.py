import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


class AffichageOrbiteTraceConnection:

    def __init__(self, positions_satellites, nb_satellites, a_satellites, b_satellites):
        self.nb_points = 1000
        self.positions_satellites = positions_satellites
        self.nb_satellites = nb_satellites
        self.a_satellites = a_satellites
        self.b_satellites = b_satellites
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.satellites = []

        # Positions initiales satellites à l'apogée
        for i in range(self.nb_satellites):
            satellite, = self.ax.plot([self.positions_satellites[i][0][-1]],
                                            [self.positions_satellites[i][1][-1]],
                                            [self.positions_satellites[i][2][-1]], 'ro',
                                            markersize=8)
            self.satellites.append(satellite)

    def tracer_orbites(self):
        for i in range(self.nb_satellites):
            self.ax.plot(self.positions_satellites[i][0], self.positions_satellites[i][1],
                         self.positions_satellites[i][2], 'b-', label='Orbite')

        # Configuration des limites des axes
        self.ax.set_xlim(-max(self.a_satellites) - 1000, max(self.a_satellites) + 1000)
        self.ax.set_ylim(-max(self.a_satellites) - 1000, max(self.a_satellites) + 1000)
        self.ax.set_zlim(-max(self.b_satellites) - 1000, max(self.b_satellites) + 1000)
        self.ax.set_aspect('auto')

    def initialiser_animation(self):
        for satellite in self.satellites:
            satellite.set_data([], [])
            satellite.set_3d_properties([])
        return self.satellites

    def update_animation(self, n):
        for i in range(self.nb_satellites):
            self.satellites[i].set_data([self.positions_satellites[i][0][n]], [self.positions_satellites[i][1][n]])
            self.satellites[i].set_3d_properties([self.positions_satellites[i][2][n]])
        return self.satellites

    def animate(self):
        self.tracer_orbites()
        anim = animation.FuncAnimation(self.fig, self.update_animation, init_func=self.initialiser_animation,
                                       frames=self.nb_points, interval=20, blit=True)
        plt.show()
