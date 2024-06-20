import numpy as np
import matplotlib.pyplot as plt


class AffichageConnectionSatellites:

    def __init__(self, satellite_1, satellite_2):
        self.satellite_1 = np.array(satellite_1)
        self.satellite_2 = np.array(satellite_2)
        self.centre_terre = [0, 0, 0]
        self.rayon_terre = 6371

    def creer_planete(self):
        # table des points des latitudes et longitudes de la planete
        # table des angles pour faire le tour de la planete
        theta = np.linspace(0, 2 * np.pi, 201)
        # valeurs de cos, sin et de zero
        cth, sth, zth = [f(theta) for f in (np.cos, np.sin, np.zeros_like)]
        lon0 = self.rayon_terre * np.vstack((cth, zth, sth))
        longs = []
        for phi in (np.pi / 180) * np.arange(0, 180, 15):
            cph, sph = [f(phi) for f in (np.cos, np.sin)]
            lon = np.vstack((lon0[0] * cph - lon0[1] * sph,
                             lon0[1] * cph + lon0[0] * sph,
                             lon0[2]))
            longs.append(lon)

        # lat0 = self.rayon_terre * np.vstack((cth, sth, zth))
        lats = []
        for phi in (np.pi / 180) * np.arange(-75, 90, 15):
            cph, sph = [f(phi) for f in (np.cos, np.sin)]
            lat = self.rayon_terre * np.vstack((cth * cph, sth * cph, zth + sph))
            lats.append(lat)

        return longs, lats

    def tracer_connection(self):
        x_coord = [self.satellite_1[0], self.satellite_2[0]]
        y_coord = [self.satellite_1[1], self.satellite_2[1]]
        z_coord = [self.satellite_1[2], self.satellite_2[2]]
        coord_terre_lon, coord_terre_lat = self.creer_planete()
        # Créer une figure 3D
        figure_1 = plt.figure()
        ax = figure_1.add_subplot(111, projection='3d')
        # Tracer les points
        ax.scatter(x_coord, y_coord, z_coord, c='r', marker='o')
        ax.plot(x_coord[:2], y_coord[:2], z_coord[:2], color="b")
        for x, y, z in coord_terre_lon:
            ax.plot(x, y, z, '-k')
        for x, y, z in coord_terre_lat:
            ax.plot(x, y, z, '-k')
        # Ajouter des labels pour les axes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Afficher la grille
        ax.grid(True)

        # Afficher le graphique
        plt.show()


    def projeter_point_droite(self):
        point = np.zeros(3)
        point_droite = np.array(self.satellite_1)
        vect = np.array(self.satellite_2-self.satellite_1)

        projection = point_droite + np.dot(point - point_droite, vect) / np.dot(vect, vect) * vect

        return projection

    def test_distance(self):
        projection_centre = self.projeter_point_droite()
        if np.linalg.norm(projection_centre) > self.rayon_terre:
            self.tracer_connection()
        else:
            print('C..n..ti.._ann.l..')


# Exemples d'utilisation
a = [6145, 6245, 6455]
b = [6145, 567, -6445]

test = AffichageConnectionSatellites(a, b)
test.test_distance()
