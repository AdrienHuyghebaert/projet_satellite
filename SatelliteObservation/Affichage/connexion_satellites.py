# ==========================================================================================
# Classe: Connexion_Satellites
# Cette classe permet de créer des objets connexion_satellites qui permettent de représenter
# la capacité de 2 satellites a communiquer entre eux et d'en créer une ligne 3D
# ==========================================================================================

import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3D

centre_terre = np.zeros(3)
rayon_terre = 6371


class ConnexionSatellites:

    def __init__(self, binome, positions_sat_1, positions_sat_2):
        self.line = None
        self.sat_1 = binome[0]
        self.sat_2 = binome[1]
        self.positions_sat_1 = positions_sat_1
        self.positions_sat_2 = positions_sat_2
        
        
    # Trace le segment 3D de connection entre 2 satellites
    def tracer_connexion_entre_satellites(self, ax, n):
        x_coords = [self.positions_sat_1[0, n],
                    self.positions_sat_2[0, n]]
        y_coords = [self.positions_sat_1[1, n],
                    self.positions_sat_2[1, n]]
        z_coords = [self.positions_sat_1[2, n],
                    self.positions_sat_2[2, n]]

        if self.line is None:  # Créer la ligne la première fois
            self.line = Line3D(x_coords, y_coords, z_coords, color='g', linewidth=2)
            ax.add_line(self.line)
        else:  # Mettre à jour la ligne
          
            # On test si la connexion est possible et on met la ligne à jours 
            if self.tester_connexion_satellites(n):
                self.line.set_data_3d(x_coords, y_coords, z_coords)
                
            # La connexion n'est pas possible, on ajoute une ligne nulle
            else:
                self.line.set_data_3d([0, 0], [0, 0], [0, 0])

        return self.line


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
        b = 2 * np.dot(vect, point_droite)
        c = np.dot(point_droite, point_droite) - rayon_terre ** 2

        # calcul du discriminant
        delta = b ** 2 - 4 * a * c

        if delta < 0:
            return [-1, 0, 0]
        elif delta == 0:
            # intersection tangente
            t = -b / (2 * a)
            point_intersection = point_droite + t * vect
            return [delta, point_intersection, 0]
        else:
            # deux points d'intersection
            t1 = (-b + np.sqrt(delta)) / (2 * a)  # coefficient du point 1
            t2 = (-b - np.sqrt(delta)) / (2 * a)  # coefficient du point 2
            point1 = point_droite + t1 * vect  # coordonnées du point 1
            point2 = point_droite + t2 * vect  # coordonnées du point 2
            return [1, point1, point2]


    # On vérifie que le point d'intersection avec le cercle trouvé précédemment est bien entre les satellites
    def tester_si_terre_entre_sat(self, pos_point, position_sat_1, position_sat_2):
        # Creation des segments à tester
        sat_1_sat_2 = position_sat_2 - position_sat_1
        sat_1_point = pos_point - position_sat_1

        # On créer le coefficient de colinéarité
        coef_col = sat_1_point/sat_1_sat_2
        # On retourne False si le point est entre les satellites
        if 1>= coef_col[1] >= 0:
            return False
        else:
            return True

    # Mise à jours de la connection entre les satellites selon les cas de test réalisés
    # On vérifie que la connection peut se faire et on met à jours en fonction du résultat
    def tester_connexion_satellites(self, n):
        x_coords = [self.positions_satellites[self.satellite_1, 0, n],
                    self.positions_satellites[self.satellite_2, 0, n]]
        y_coords = [self.positions_satellites[self.satellite_1, 1, n],
                    self.positions_satellites[self.satellite_2, 1, n]]
        z_coords = [self.positions_satellites[self.satellite_1, 2, n],
                    self.positions_satellites[self.satellite_2, 2, n]]

        # On crée les tables de position des satellites
        position_sat_1 = np.array([x_coords[0], y_coords[0], z_coords[0]])
        position_sat_2 = np.array([x_coords[1], y_coords[1], z_coords[1]])

        # Segment entre les deux satellites et choix du satellite le plus éloigné
        dist_sat_1 = np.abs(np.linalg.norm(position_sat_1))
        dist_sat_2 = np.abs(np.linalg.norm(position_sat_2))
        if dist_sat_1 > dist_sat_2:
            vect = np.array(position_sat_1 - position_sat_2)
            position_sat_ref = position_sat_1
            autre_sat = position_sat_2
        else:
            vect = np.array(position_sat_2 - position_sat_1)
            position_sat_ref = position_sat_2
            autre_sat = position_sat_1

        # On test si la droite de connection passe par la Terre
        test_intersection = self.intersection_ligne_cercle(vect, position_sat_ref)

        # La droite ne passe pas par la Terre, on a la connection
        if test_intersection[0] == -1 :
            return True

        # La droite par la Terre, il faut vérifier si cela se fait entre les satellites ou non
        elif test_intersection[0] == 0:
            # Le point d'intersection entre la droite et la Terre n'est pas entre les satellites, on a la connection
            if self.tester_si_terre_entre_sat(test_intersection[1], position_sat_ref, autre_sat):
                return True
            # Le point d'intersection entre la droite et la Terre est entre les satellites, pas de connection
            else:
                return False
        else:
            # Tous les points d'intersections entre la droite et la Terre ne sont pas entre les satellites, on a la connection
            if self.tester_si_terre_entre_sat(test_intersection[1], position_sat_ref, autre_sat) and self.tester_si_terre_entre_sat(test_intersection[2], position_sat_ref, autre_sat):
                return True
            # Au moins un des points d'intersections entre la droite et la Terre est entre les satellites, pas de connection
            else:
                return False
   