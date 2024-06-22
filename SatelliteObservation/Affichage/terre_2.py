import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3D


class Terre:
    def __init__(self):
        self.rayon_terre = 6371
        self.line = None

    def creer_geometrie_terre(self):
        # table des points des latitudes et longitudes de la planète
        # table des angles pour faire le tour de la planète
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

    def afficher_terre(self, ax):
        # Affichage
        for x, y, z in self.creer_geometrie_terre()[0]:
            self.line = Line3D(x, y, z, color='k')
            ax.add_line(self.line)
        for x, y, z in self.creer_geometrie_terre()[1]:
            self.line = Line3D(x, y, z, color='k')
            ax.add_line(self.line)
        return self.line
