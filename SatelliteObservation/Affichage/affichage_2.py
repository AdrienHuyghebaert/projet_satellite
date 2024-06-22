import matplotlib.animation as animation
from matplotlib import pyplot as plt
import numpy as np
from .connexion_satellites import ConnexionSatellites
from .affichage_terre import afficher_terre

#Constantes

nb_points = 1000


class AffichageOrbiteTraceConnexion2:
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

        # Création des objets ConnexionSatellites
        if self.aff_connexions:  # Si True alors on rentre
            for i in range(len(self.positions_satellites)):
                for j in range(i + 1, len(self.positions_satellites)):  # Éviter les connexions doubles et les auto-connexions
                    self.binomes_satellites.append((i, j))  # Ajouter chaque couple unique de satellites
                    connexion = ConnexionSatellites((i, j), self.positions_satellites)  # Création de l'objet connexion
                    self.lignes_connexion[(i, j)] = connexion  # Ajout de l'objet connexion dans le dictionnaire

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

    def initialiser_animation(self):
        artists = []

        # Initialisation animation des satellites
        for satellite in self.satellites:
            satellite.set_data([], [])
            satellite.set_3d_properties([])
            artists.append(satellite)

        # Initialisation animation des connexions entre les satellites
        if self.aff_connexions:
            for connexion in self.binomes_satellites:
                line = self.lignes_connexion[connexion].tracer_connexion_entre_satellites(self.ax)
                artists.append(line)

        return artists

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

        # Mettre à jour toutes les lignes de connexion entre les satellites
        if self.aff_connexions:
            for connexion in self.binomes_satellites:
                line = self.lignes_connexion[connexion].mettre_a_jour_connexions(n)
                artists.append(line)

        return artists

    def animate(self):
        self.tracer_orbites()
        if self.aff_terre:
            self.afficher_terre()
        anim = animation.FuncAnimation(self.fig, self.update_animation, init_func=self.initialiser_animation,
                                       frames=nb_points, interval=20, blit=True)
        plt.show()
