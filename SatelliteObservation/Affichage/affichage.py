import matplotlib.pyplot as plt
import matplotlib.animation as animation
from .affichage_terre import *

rayon_terre = 6371
centre_terre = np.array([0, 0, 0])


class AffichageOrbiteTraceConnection:
    def __init__(self, positions_satellites, nb_satellites, a_satellites, b_satellites):
        self.nb_points = 1000
        self.positions_satellites = np.array(positions_satellites)  # Convertir en tableau Numpy
        self.nb_satellites = nb_satellites
        self.a_satellites = a_satellites
        self.b_satellites = b_satellites
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.satellites = []
        self.satellite_connections = []  # Liste des connexions entre les satellites
        self.connection_lines = {}  # Dictionnaire pour stocker les lignes de connexion

        # Initialisation des positions initiales des satellites avec un décalage aléatoire
        for i in range(self.nb_satellites):
            decalage = np.random.randint(self.nb_points)
            self.positions_satellites[i] = np.roll(self.positions_satellites[i], -decalage, axis=1)  # CHAT.GPT
            satellite, = self.ax.plot([self.positions_satellites[i, 0, -1]],
                                      [self.positions_satellites[i, 1, -1]],
                                      [self.positions_satellites[i, 2, -1]], 'ro',
                                      markersize=8)
            self.satellites.append(satellite)

        # Initialisation des connexions entre les satellites
        for i in range(self.nb_satellites):
            for j in range(i + 1, self.nb_satellites):  # Éviter les connexions doubles et les auto-connexions
                self.satellite_connections.append((i, j))  # Ajouter chaque couple unique de satellites
                self.tracer_droite_entre_satellites(i, j)  # Créer la ligne initiale entre les 2 satellites

    def afficher_terre(self):
        coord_terre_lon, coord_terre_lat = afficher_terre()
        for x, y, z in coord_terre_lon:
            self.ax.plot(x, y, z, '-k')
        for x, y, z in coord_terre_lat:
            self.ax.plot(x, y, z, '-k')

    def tracer_orbites(self):
        for i in range(self.nb_satellites):
            self.ax.plot(self.positions_satellites[i, 0], self.positions_satellites[i, 1],
                         self.positions_satellites[i, 2], 'b-', label='Orbite')

        max_a = np.max(self.a_satellites)
        max_b = np.max(self.b_satellites)
        self.ax.set_xlim(-max_a - 1000, max_a + 1000)
        self.ax.set_ylim(-max_a - 1000, max_a + 1000)
        self.ax.set_zlim(-max_b - 1000, max_b + 1000)
        self.ax.set_aspect('auto')

    def tracer_droite_entre_satellites(self, satellite1_idx, satellite2_idx):
        x_coords = [self.positions_satellites[satellite1_idx, 0, -1], self.positions_satellites[satellite2_idx, 0, -1]]
        y_coords = [self.positions_satellites[satellite1_idx, 1, -1], self.positions_satellites[satellite2_idx, 1, -1]]
        z_coords = [self.positions_satellites[satellite1_idx, 2, -1], self.positions_satellites[satellite2_idx, 2, -1]]

        # Création de la nouvelle ligne (ou MAJ) de la ligne dans le dictionnaire
        line, = self.ax.plot(x_coords, y_coords, z_coords, 'g-', linewidth=2)
        self.connection_lines[(satellite1_idx, satellite2_idx)] = line

    def initialiser_animation(self):
        for satellite in self.satellites:
            satellite.set_data([], [])
            satellite.set_3d_properties([])
        return self.satellites

    def update_animation(self, n):
        artists = []

        # Mise à jour des positions des satellites
        for i in range(self.nb_satellites):
            x = self.positions_satellites[i, 0, n]
            y = self.positions_satellites[i, 1, n]
            z = self.positions_satellites[i, 2, n]

            self.satellites[i].set_data([x], [y])
            self.satellites[i].set_3d_properties([z])
            artists.append(self.satellites[i])

        # Mettre à jour toutes les lignes de connexion entre les satellites
        # en parcourant chaque binôme
        for connection in self.satellite_connections:
            satellite1_idx, satellite2_idx = connection
            x_coords = [self.positions_satellites[satellite1_idx, 0, n],
                        self.positions_satellites[satellite2_idx, 0, n]]
            y_coords = [self.positions_satellites[satellite1_idx, 1, n],
                        self.positions_satellites[satellite2_idx, 1, n]]
            z_coords = [self.positions_satellites[satellite1_idx, 2, n],
                        self.positions_satellites[satellite2_idx, 2, n]]

            self.connection_lines[(satellite1_idx, satellite2_idx)].set_data(x_coords, y_coords)
            self.connection_lines[(satellite1_idx, satellite2_idx)].set_3d_properties(z_coords)
            artists.append(self.connection_lines[(satellite1_idx, satellite2_idx)])

        return artists

    def animate(self):
        self.tracer_orbites()
        self.afficher_terre()
        anim = animation.FuncAnimation(self.fig, self.update_animation, init_func=self.initialiser_animation,
                                       frames=self.nb_points, interval=20, blit=True)
        plt.show()
