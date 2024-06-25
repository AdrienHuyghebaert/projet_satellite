import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3D

# Ajouter pour tracer en dehors du main
# import matplotlib.pyplot as plt

# Constantes
rayon_terre = 6371  # km
angle_antenne = 160 # °
resolution = 50  # nbr de points sur le cercle


class Antenne:
    def __init__(self, position_satellite):
        self.position_satellite = position_satellite
        self.angle_antenne =  angle_antenne
        self.resolution = resolution
        self.rayon_planete = rayon_terre
        self.line = None


    # Cette fonction a été créé en partie avec l'utilisation de ChatGPT :
    # prompt : tracer un cercle avec un angle dans l'espace 3D
    def creer_cercle(self):

        # On convertit l'angle de l'antenne en radiant
        angle_antenne_rad = self.angle_antenne * np.pi / 360

        # création du vecteur normal au cercle de projection
        centre_planete = np.zeros(3)
        vect_direction = np.array(self.position_satellite) - centre_planete
        vect_cone = self.tourner_ligne_theta(vect_direction, angle_antenne_rad)

        # creation des points correspondants au cercle projeté sur la Terre par le cone de l'antenne du satellite
        point_intersection_cercle = self.intersection_ligne_cercle(vect_cone)
        print(point_intersection_cercle)
        point_projete = self.projeter_point_droite(point_intersection_cercle, vect_direction)

        # On crée deux vecteurs perpendiculaires dans le plan pour tracer le cercle
        vect_direction_norm = vect_direction/np.linalg.norm(vect_direction)  # Vecteur direction normé entre le centre de la terre et du satellite
        v1_plan_cercle = point_projete - point_intersection_cercle  # Vecteur appartenant au plan du cercle de projection
        v1_plan_cercle = v1_plan_cercle/np.linalg.norm(v1_plan_cercle)  # On norme le vecteur
        v2_plan_cercle = np.cross(vect_direction_norm, v1_plan_cercle)  # Vecteur perpendiculaire qui permettra de créer le cercle dans le plan de normale
        rayon_cercle = np.linalg.norm(point_projete - point_intersection_cercle)

        # Angle theta discretisé pour le tracé du cercle
        theta = np.linspace(0, 2 * np.pi, self.resolution)

        # Positions paramétriques du cercle
        pos_x = point_projete[0] + rayon_cercle * (v1_plan_cercle[0] * np.cos(theta) + v2_plan_cercle[0] * np.sin(theta))
        pos_y = point_projete[1] + rayon_cercle * (v1_plan_cercle[1] * np.cos(theta) + v2_plan_cercle[1] * np.sin(theta))
        pos_z = point_projete[2] + rayon_cercle * (v1_plan_cercle[2] * np.cos(theta) + v2_plan_cercle[2] * np.sin(theta))

        return pos_x, pos_y, pos_z

    # Cette fonction à été réalisée à l'aide de ChatGPT
    # prompt : coordonnées d'un point d'intersection entre une droite et un cercle
    # Pour réaliser le calcul d'intersection entre la droite du cone et le cercle de la terre
    # on utilise la résolution d'une équation de second degrès (voir https://www.youtube.com/watch?v=zIsBk05vvjw)
    def intersection_ligne_cercle(self, vect_direction):
        # paramètres de la droite
        point_droite = np.array(self.position_satellite)
        vect = np.array(vect_direction)
        # calcul des coeff du système d'équation
        a = np.dot(vect, vect)
        b = 2*np.dot(vect, point_droite)
        c = np.dot(point_droite, point_droite) - rayon_terre**2

        # calcul du discriminant
        delta = b**2 - 4*a*c

        if delta < 0:
            # Pas d'intersection réelle, on
            if self.position_satellite[0]<0 :
                return [-rayon_terre, 0, 0]
            else:
                return [rayon_terre, 0, 0]
        elif delta == 0:
            # intersection tangente
            t = -b/(2*a)
            point_intersection = point_droite + t*vect
            return point_intersection
        else:
            # deux points d'intersection
            t1 = (-b + np.sqrt(delta)) / (2*a)
            t2 = (-b - np.sqrt(delta)) / (2*a)
            point1 = point_droite + t1*vect
            point2 = point_droite + t2*vect
            dist1 = point_droite - point1
            dist2 = point_droite - point2
            if np.linalg.norm(dist1) > np.linalg.norm(dist2):
                return point2
            else:
                return point1


    def projeter_point_droite(self, point, droite):
        point = np.array(point)
        point_droite = np.array(self.position_satellite)
        vect = np.array(droite)

        projection = point_droite + np.dot(point - point_droite, vect) / np.dot(vect, vect) * vect

        return projection


    def tourner_ligne_theta(self, direction, theta):
        # On converti les données
        # origine = np.array(self.position_satellite)
        direction = np.array(direction)

        # on calcule la matrice de rotation
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        matrice_rotation = np.array([[cos_theta, -sin_theta, 0],
                                    [sin_theta, cos_theta, 0],
                                    [0, 0, 1]])

        # Appliquer la rotation à la droite
        direction_modif = np.dot(matrice_rotation, direction)

        return direction_modif

    def tracer_cercle_antenne(self, ax):
        x_coords, y_coords, z_coords = self.creer_cercle()

        if self.line is None:  # Créer la ligne la première fois
            self.line = Line3D(x_coords, y_coords, z_coords, color='r', linewidth=2)
            ax.add_line(self.line)
        else:  # Mettre à jour la ligne
            self.line.set_data_3d(x_coords, y_coords, z_coords)

        return self.line

# Tracer en dehors du main
'''
    def tracer_cercle(self):
        # On récupère les coordonnées du cercle à partir de la fonction creer_cercle()
        x_coord, y_coord, z_coord = self.creer_cercle()

        # Créer une figure 3D
        figure_1 = plt.figure(1)
        ax = figure_1.add_subplot(111, projection='3d')
        coord_terre_lon, coord_terre_lat = self.creer_planete()
        # Tracer les points
        ax.plot(x_coord, y_coord, z_coord, '-r')

        # Tracer la Terre
        for x, y, z in coord_terre_lon:
            ax.plot(x, y, z, '-k')
        for x, y, z in coord_terre_lat:
            ax.plot(x, y, z, '-k')

        # Tracer le sat
        ax.plot(self.position_satellite[0], self.position_satellite[1], self.position_satellite[2], c='r', marker='o')
        # Ajouter des labels pour les axes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Afficher la grille
        ax.grid(True)

        # Afficher le graphique
        plt.show()

    def creer_planete(self):
        # table des points des latitudes et longitudes de la planete
        # table des angles pour faire le tour de la planete
        theta = np.linspace(0, 2 * np.pi, 201)
        # valeurs de cos, sin et de zero
        cth, sth, zth = [f(theta) for f in (np.cos, np.sin, np.zeros_like)]
        lon0 = self.rayon_planete * np.vstack((cth, zth, sth))
        longs = []
        for phi in (np.pi / 180) * np.arange(0, 180, 15):
            cph, sph = [f(phi) for f in (np.cos, np.sin)]
            lon = np.vstack((lon0[0] * cph - lon0[1] * sph,
                             lon0[1] * cph + lon0[0] * sph,
                             lon0[2]))
            longs.append(lon)

        # lat0 = rayon_planete * np.vstack((cth, sth, zth))
        lats = []
        for phi in (np.pi / 180) * np.arange(-75, 90, 15):
            cph, sph = [f(phi) for f in (np.cos, np.sin)]
            lat = self.rayon_planete * np.vstack((cth * cph, sth * cph, zth + sph))
            lats.append(lat)

        return longs, lats
'''