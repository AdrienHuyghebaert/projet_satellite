import numpy as np


def afficher_terre():
    # table des points des latitudes et longitudes de la planete
    # table des angles pour faire le tour de la planete
    theta = np.linspace(0, 2 * np.pi, 201)
    rayon_terre = 6371

    # valeurs de cos, sin et de zero
    cth, sth, zth = [f(theta) for f in (np.cos, np.sin, np.zeros_like)]
    lon0 = rayon_terre * np.vstack((cth, zth, sth))
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
        lat = rayon_terre * np.vstack((cth * cph, sth * cph, zth + sph))
        lats.append(lat)

    return longs, lats
