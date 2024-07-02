import numpy as np

# Variables communes

rayon_terre = 6374.2  # Rayon de la Terre en km
masse_terre = 5.974 * (10 ** 24)  # Masse de la Terre en kg
G = 6.67 * 10 ** (-11)  # Constante gravitationnelle universelle
g = 9.81  # en m/s2


class Satellite:

    def __init__(self, apogee, perigee, inclinaison):
        self.apogee = apogee
        self.perigee = perigee
        self.inclinaison = inclinaison

    def calcul_rayons_ellipse(self):
        r_a = self.apogee + rayon_terre
        r_p = self.perigee + rayon_terre
        return r_a, r_p

    def calcul_mu(self):
        mu = G * masse_terre  # on fait l'hypothèse que la masse du satellite est négligeable
        return mu

    def calcul_parametres_ellipse(self):
        r_a, r_p = self.calcul_rayons_ellipse()
        a = (r_a + r_p) / 2  # Demi-grand axe
        e = (r_a - r_p) / (r_a + r_p)  # Excentricité
        b = a * np.sqrt(1 - e ** 2)  # Demi-petit axe
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
