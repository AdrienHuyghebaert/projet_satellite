import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3D


# Constantes (pourraient être initialisées dans l'avenir
rayon_terre = 6371  # km
angle_antenne = 13 # °
resolution = 50  # nbr de points sur le cercle


class Antenne:
    def __init__(self, positions_satellite):
        self.positions_satellite = positions_satellite
        self.angle_antenne =  angle_antenne
        self.resolution = resolution
        self.rayon_planete = rayon_terre
        self.line = None


    # Cette fonction a été créé en partie avec l'utilisation de ChatGPT :
    # prompt : tracer un cercle avec un angle dans l'espace 3D
    def creer_cercle(self, position_satellite):

        # On convertit l'angle de l'antenne en radiant
        angle_antenne_rad = self.angle_antenne * np.pi / 360

        # création du vecteur normal au cercle de projection
        centre_planete = np.zeros(3)
        vect_direction = np.array(position_satellite) - centre_planete
        vect_cone = self.tourner_ligne_theta(vect_direction, angle_antenne_rad)

        # creation des points correspondants au cercle projeté sur la Terre par le cone de l'antenne du satellite
        point_intersection_cercle = self.intersection_ligne_cercle(vect_cone, position_satellite)

        # Disjontion de cas si l'antenne couvre toute la planette
        if np.all(point_intersection_cercle == np.zeros(3)):

            # On crée deux vecteurs perpendiculaires dans le plan pour tracer le cercle
            vect_direction_norm = vect_direction / np.linalg.norm(vect_direction)  # Vecteur direction normé entre le centre de la terre et du satellite
            vect_alea = np.array([1, 0, 0]) if not np.all(vect_direction_norm == [1, 0, 0]) else np.array([0, 1, 0])
            v1_plan_cercle = np.cross(vect_direction_norm, vect_alea)
            v1_plan_cercle = v1_plan_cercle/np.linalg.norm(v1_plan_cercle)
            v2_plan_cercle = np.cross(vect_direction_norm, v1_plan_cercle)
            v2_plan_cercle = v2_plan_cercle / np.linalg.norm(v2_plan_cercle)
            rayon_cercle = rayon_terre

            # Angle theta discretisé pour le tracé du cercle
            theta = np.linspace(0, 2 * np.pi, self.resolution)

            # Positions paramétriques du cercle
            pos_x = point_projete[0] + rayon_cercle * (v1_plan_cercle[0] * np.cos(theta) + v2_plan_cercle[0] * np.sin(theta))
            pos_y = point_projete[1] + rayon_cercle * (v1_plan_cercle[1] * np.cos(theta) + v2_plan_cercle[1] * np.sin(theta))
            pos_z = point_projete[2] + rayon_cercle * (v1_plan_cercle[2] * np.cos(theta) + v2_plan_cercle[2] * np.sin(theta))

        else:
            point_projete = self.projeter_point_droite(point_intersection_cercle, vect_direction, position_satellite)

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
    def intersection_ligne_cercle(self, vect_direction, position_satellite):
        # paramètres de la droite
        point_droite = np.array(position_satellite)
        vect = np.array(vect_direction)
        # calcul des coeff du système d'équation
        a = np.dot(vect, vect)
        b = 2*np.dot(vect, point_droite)
        c = np.dot(point_droite, point_droite) - rayon_terre**2

        # calcul du discriminant
        delta = b**2 - 4*a*c

        if delta < 0:
            # Pas d'intersection réelle, on doit donc tracer un cercle qui couvre toute la Terre
            return np.zeros(3)
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


    def projeter_point_droite(self, point, droite, position_satellite):
        point = np.array(point)
        point_droite = np.array(position_satellite)
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

    def tracer_cercle_antenne(self, ax, n):
        # Position de l'antenne pour n
        position_satellite = np.array([self.positions_satellite[0, n],
                                       self.positions_satellite[1, n],
                                       self.positions_satellite[2, n]])
        x_coords, y_coords, z_coords = self.creer_cercle(position_satellite)

        if self.line is None:  # Créer la ligne la première fois
            self.line = Line3D(x_coords, y_coords, z_coords, color='r', linewidth=2)
            ax.add_line(self.line)
        else:  # Mettre à jour la ligne
            self.line.set_data_3d(x_coords, y_coords, z_coords)

        return self.line
