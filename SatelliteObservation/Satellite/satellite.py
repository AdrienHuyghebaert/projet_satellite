import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Variables communes

rayon_terre = 6374.2  # Rayon de la Terre en km
masse_terre = 5.974 * (10 ** 24)  # Masse de la Terre en kg
G = 6.67 * 10 ** (-11)  # Constante gravitationnelle universelle
g = 9.81  # en m/s2


class Satellite:

    def __init__(self, apogee, perigee, e, inclinaison, masse):
        self.apogee = apogee
        self.perigee = perigee
        self.e = e
        self.inclinaison = inclinaison
        self.masse = masse

    def calcul_rayons_ellipse(self):
        r_a = self.apogee + rayon_terre
        r_p = self.perigee + rayon_terre
        return r_a, r_p

    def calcul_mu(self):
        mu = G * (self.masse + masse_terre)
        return mu

    def calcul_parametres_ellipse(self):
        r_a, r_p = self.calcul_rayons_ellipse()
        a = (r_a + r_p) / 2  # Demi-grand axe
        e = (r_a - r_p) / (r_a + r_p)  # Excentricité
        b = a * np.sqrt(1 - e**2)  # Demi-petit axe
        print(a, b, e)
        return a, b, e

    def conversion_deg_to_rad(self):
        inclinaison_rad = np.radians(self.inclinaison)
        return inclinaison_rad

    def calcul_coord_ellipse(self):
        num_points = 1000
        t = np.linspace(0, 2 * np.pi, num_points)
        a, b, e = self.calcul_parametres_ellipse()
        x = a * np.cos(t) + a - self.calcul_parametres_ellipse()[1]
        y = b * np.sin(t)
        z = np.zeros_like(x)

        return x, y, z

    def calcul_coord_ellipse_inclinee(self):
        x, y, z = self.calcul_coord_ellipse()
        inclinaison = self.conversion_deg_to_rad()
        x_inclined = x
        y_inclined = y * np.cos(inclinaison)
        z_inclined = y * np.sin(inclinaison)
        tableau_positions = np.array([x_inclined, y_inclined, z_inclined])
        return x_inclined, y_inclined, z_inclined, tableau_positions

    def tracer_orbite_3d(self):
        num_points = 1000
        a, b, e = self.calcul_parametres_ellipse()
        x_inclined, y_inclined, z_inclined = self.calcul_coord_ellipse_inclinee()[:3]

        # Animation de la position du satellite le long de l'orbite
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Tracer l'orbite inclinée
        ax.plot(x_inclined, y_inclined, z_inclined, 'b-', label='Orbite')

        # Position initiale du satellite (à l'apogée)
        satellite, = ax.plot([x_inclined[-1]], [y_inclined[-1]], [z_inclined[-1]], 'ro', markersize=8)

        # Configuration des limites des axes
        ax.set_xlim(-a - 1000, a + 1000)
        ax.set_ylim(-a - 1000, a + 1000)
        ax.set_zlim(-b - 1000, b + 1000)
        ax.set_aspect('auto')

        # Fonction d'initialisation de l'animation
        def init():
            satellite.set_data([], [])
            satellite.set_3d_properties([])
            return satellite,

        # Fonction d'animation
        def animate(i):
            satellite.set_data([x_inclined[i]], [y_inclined[i]])
            satellite.set_3d_properties([z_inclined[i]])
            return satellite,

        # Création de l'animation avec FuncAnimation
        ani = animation.FuncAnimation(fig, animate, frames=num_points, init_func=init, interval=20, blit=True)

        # Afficher l'animation
        plt.show()


# Exemple d'utilisation de la classe Satellite
# satellite = Satellite(200100, 400, 0.9, 45, 50)
#
# print("Rayons de l'ellipse:", satellite.calcul_rayons_ellipse())
# print("Paramètres de l'ellipse:", satellite.calcul_parametres_ellipse())
# satellite.tracer_orbite_3d()