import matplotlib.pyplot as plt
import matplotlib.animation as animation
from .affichage_terre import *

rayon_terre = 6371
centre_terre = np.zeros(3)
nb_points = 1000


class AffichageOrbiteTraceConnection:
    def __init__(self, positions_satellites, a_satellites, b_satellites, aff_connexions, aff_terre):
        self.positions_satellites = positions_satellites
        self.a_satellites = a_satellites
        self.b_satellites = b_satellites
        self.aff_connexions = aff_connexions  # Paramètre pour gérer ou non l'affichage des connexions
        self.aff_terre = aff_terre  # Paramètre pour gérer ou non l'affichage de la Terre

        self.satellites = []  # Liste pour stocker les satellites
        self.binomes_satellites = []  # Liste des connexions entre les satellites
        self.lignes_connexion = {}  # Dictionnaire pour stocker les lignes de connexion

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        # Initialisation des positions initiales des satellites avec un décalage aléatoire
        for i in range(len(self.positions_satellites)):
            self.decalage = np.random.randint(nb_points)
            self.positions_satellites[i] = np.roll(self.positions_satellites[i], -self.decalage, axis=1)
            satellite, = self.ax.plot([self.positions_satellites[i, 0, -1]],
                                      [self.positions_satellites[i, 1, -1]],
                                      [self.positions_satellites[i, 2, -1]], 'ro',
                                      markersize=8)
            self.satellites.append(satellite)

        # Initialisation des connexions entre les satellites
        if self.aff_connexions:  # Si True alors on rentre
            for i in range(len(self.positions_satellites)):
                for j in range(i + 1, len(self.positions_satellites)):  # Éviter les connexions doubles et les auto-connexions
                    self.binomes_satellites.append((i, j))  # Ajouter chaque couple unique de satellites
                    self.tracer_connexion_entre_satellites(i, j)  # Créer la ligne initiale entre les 2 satellites

    def afficher_terre(self):
        coord_terre_lon, coord_terre_lat = afficher_terre()
        for x, y, z in coord_terre_lon:
            self.ax.plot(x, y, z, '-k')
        for x, y, z in coord_terre_lat:
            self.ax.plot(x, y, z, '-k')

    def tracer_orbites(self):
        for i in range(len(self.positions_satellites)):
            self.ax.plot(self.positions_satellites[i, 0], self.positions_satellites[i, 1],
                         self.positions_satellites[i, 2], 'b-', label='Orbite')

        max_a = np.max(self.a_satellites)
        max_b = np.max(self.b_satellites)
        self.ax.set_xlim(-max_a - 1000, max_a + 1000)
        self.ax.set_ylim(-max_a - 1000, max_a + 1000)
        self.ax.set_zlim(-max_b - 1000, max_b + 1000)
        self.ax.set_aspect('auto')

    def tracer_connexion_entre_satellites(self, satellite1_idx, satellite2_idx):
        x_coords = [self.positions_satellites[satellite1_idx, 0, -1], self.positions_satellites[satellite2_idx, 0, -1]]
        y_coords = [self.positions_satellites[satellite1_idx, 1, -1], self.positions_satellites[satellite2_idx, 1, -1]]
        z_coords = [self.positions_satellites[satellite1_idx, 2, -1], self.positions_satellites[satellite2_idx, 2, -1]]

        # Création de la nouvelle ligne (ou MAJ) de la ligne dans le dictionnaire
        line, = self.ax.plot(x_coords, y_coords, z_coords, 'g-', linewidth=2)
        self.lignes_connexion[(satellite1_idx, satellite2_idx)] = line

    def tester_connexion_satellites(self, position_sat_1, position_sat_2):
        # On définit le centre de la Terre à projeter sur la droite de connection entre les satellites
        point_centre = centre_terre
        point_droite = np.array(position_sat_1)

        # On définit la droite de connection entre les satellites
        vect = np.array(position_sat_2 - position_sat_1)

        # On projette le point sur la droite et on récupère ses coordonnées
        projection = point_droite + np.dot(point_centre - point_droite, vect) / np.dot(vect, vect) * vect

        # On calcule la distance entre le centre et le point projette
        distance = np.linalg.norm(projection - point_centre)

        return distance

    def initialiser_animation(self):
        for satellite in self.satellites:
            satellite.set_data([], [])
            satellite.set_3d_properties([])
        return self.satellites

    # Cette fonction permet de savoir si la droite entre les 2 satellites traverse oui ou non la Terre

    def update_animation(self, n):
        artists = []

        # Mise à jour des positions des satellites
        for i in range(len(self.positions_satellites)):
            x = self.positions_satellites[i, 0, n]
            y = self.positions_satellites[i, 1, n]
            z = self.positions_satellites[i, 2, n]

            self.satellites[i].set_data([x], [y])
            self.satellites[i].set_3d_properties([z])
            artists.append(self.satellites[i])

        if self.aff_connexions:
            # Mettre à jour toutes les lignes de connexion entre les satellites
            # en parcourant chaque binôme
            for connexion in self.binomes_satellites:
                satellite1_idx, satellite2_idx = connexion
                x_coords = [self.positions_satellites[satellite1_idx, 0, n],
                            self.positions_satellites[satellite2_idx, 0, n]]
                y_coords = [self.positions_satellites[satellite1_idx, 1, n],
                            self.positions_satellites[satellite2_idx, 1, n]]
                z_coords = [self.positions_satellites[satellite1_idx, 2, n],
                            self.positions_satellites[satellite2_idx, 2, n]]

                position_sat_1 = np.array([x_coords[0], y_coords[0], z_coords[0]])
                position_sat_2 = np.array([x_coords[1], y_coords[1], z_coords[1]])
                distance = self.tester_connexion_satellites(position_sat_1, position_sat_2)

                if distance > rayon_terre:
                    self.lignes_connexion[(satellite1_idx, satellite2_idx)].set_data(x_coords, y_coords)
                    self.lignes_connexion[(satellite1_idx, satellite2_idx)].set_3d_properties(z_coords)
                    artists.append(self.lignes_connexion[(satellite1_idx, satellite2_idx)])
                else:
                    self.lignes_connexion[(satellite1_idx, satellite2_idx)].set_data([0, 0], [0, 0])
                    self.lignes_connexion[(satellite1_idx, satellite2_idx)].set_3d_properties([0, 0])
                    artists.append(self.lignes_connexion[(satellite1_idx, satellite2_idx)])

        return artists

    def animate(self):
        self.tracer_orbites()
        if self.aff_terre:
            self.afficher_terre()
        anim = animation.FuncAnimation(self.fig, self.update_animation, init_func=self.initialiser_animation,
                                       frames=nb_points, interval=20, blit=True)
        plt.show()
