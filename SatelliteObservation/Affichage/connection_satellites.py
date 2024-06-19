import numpy as np
import matplotlib.pyplot as plt


def distance_centre_ligne(point0, point1, point2):
    centre = np.array(point0)
    point1 = np.array(point1)
    point2 = np.array(point2)
    vect_droite = point2 - point1
    vect_centre = centre - point1
    distance = np.linalg.norm(np.cross(vect_droite, vect_centre))/np.linalg.norm(vect_centre)
    return distance


def tester_connection(centre_sphere, rayon_planete, point1, point2):
    """Checks if a line passes through a sphere."""
    distance = distance_centre_ligne(centre_sphere, point1, point2)
    return distance <= rayon_planete


def creer_planete(rayon_planete):
    # table des points des latitudes et longitudes de la planete
    # table des angles pour faire le tour de la planete
    theta = np.linspace(0, 2*np.pi, 201)
    # valeurs de cos, sin et de zero
    cth, sth, zth = [f(theta) for f in (np.cos, np.sin, np.zeros_like)]
    lon0 = rayon_planete * np.vstack((cth, zth, sth))
    longs = []
    for phi in (np.pi/180) * np.arange(0, 180, 15):
        cph, sph = [f(phi) for f in (np.cos, np.sin)]
        lon = np.vstack((lon0[0] * cph - lon0[1] * sph,
                         lon0[1] * cph + lon0[0] * sph,
                         lon0[2]))
        longs.append(lon)

    # lat0 = rayon_planete * np.vstack((cth, sth, zth))
    lats = []
    for phi in (np.pi/180) * np.arange(-75, 90, 15):
        cph, sph = [f(phi) for f in (np.cos, np.sin)]
        lat = rayon_planete * np.vstack((cth * cph, sth * cph, zth + sph))
        lats.append(lat)

    return longs, lats


def tracer_connection(point1, point2):
    x_coord = [point1[0], point2[0]]
    y_coord = [point1[1], point2[1]]
    z_coord = [point1[2], point2[2]]
    coord_terre_lon, coord_terre_lat = creer_planete(rayon_terre)
    # Créer une figure 3D
    figure_1 = plt.figure(1,figsize=[10, 8])
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


# Exemples d'utilisation
a = [6145, 6245, 6455]  #km
b = [-6445, -6445, -6445]  #km
rayon_terre = 6371  #km
c = [0, 0, 0]  #km

x_coord = [a[0], b[0], c[0]]
y_coord = [a[1], b[1], c[1]]
z_coord = [a[2], b[2], c[2]]


if tester_connection(c, rayon_terre, a, b):
    print("La droite passe à travers la sphère.")
else:
    print("La droite ne passe pas à travers la sphère.")
    tracer_connection(a, b)

