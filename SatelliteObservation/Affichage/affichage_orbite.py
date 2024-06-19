import matplotlib.pyplot as plt
import matplotlib.animation as animation


class AffichageOrbiteSatellite:

    # Récupération des données d'entrée et initialisation de la figure

    def __init__(self, nb_points, a, b, x_inclined, y_inclined, z_inclined):
        self.nb_points = nb_points
        self.a = a
        self.b = b
        self.x_inclined = x_inclined
        self.y_inclined = y_inclined
        self.z_inclined = z_inclined
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        # Tracer l'orbite inclinée
        self.ax.plot(self.x_inclined, self.y_inclined, self.z_inclined, 'b-', label='Orbite')

        # Position initiale du satellite (à l'apogée)
        self.satellite, = self.ax.plot([self.x_inclined[-1]], [self.y_inclined[-1]], [self.z_inclined[-1]], 'ro',
                                       markersize=8)

    def get_data(self):
        # Configuration des limites des axes
        self.ax.set_xlim(-self.a - 1000, self.a + 1000)
        self.ax.set_ylim(-self.a - 1000, self.a + 1000)
        self.ax.set_zlim(-self.b - 1000, self.b + 1000)
        self.ax.set_aspect('auto')

    # Affichage initial du satellite
    def ani_init(self):
        self.satellite.set_data([], [])
        self.satellite.set_3d_properties([])

        return self.satellite,

    # Mise à jour de l'affichage du satellite
    def ani_update(self, i):
        self.satellite.set_data([self.x_inclined[i]], [self.y_inclined[i]])
        self.satellite.set_3d_properties([self.z_inclined[i]])

        return self.satellite,

    # Fonction d'animation
    def animate(self):
        anim = animation.FuncAnimation(self.fig, self.ani_update, init_func=self.ani_init, frames=self.nb_points,
                                       interval=20, blit=True)
        plt.show()
