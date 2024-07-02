import matplotlib.animation as animation
from matplotlib import pyplot as plt
from .connexion_satellites import ConnexionSatellites
from .terre_2 import *
from .orbite import *
from .antenne import Antenne

# Constantes
nb_points = 1000


class AffichageOrbiteTraceConnexion2:
    def __init__(self, positions_satellites, a_satellites, b_satellites, aff_connexions, aff_terre, aff_orbite, aff_antenne):
        self.positions_satellites = positions_satellites
        self.a_satellites = a_satellites
        self.b_satellites = b_satellites
        self.aff_connexions = aff_connexions  # Paramètre pour gérer ou non l'affichage des connexions
        self.aff_terre = aff_terre  # Paramètre pour gérer ou non l'affichage de la Terre
        self.aff_orbite = aff_orbite  # Paramètre pour gérer ou non l'affichage des orbites
        self.aff_antenne = aff_antenne  # Paramètre pour gérer ou non l'affichage des antennes

        self.satellites = []  # Liste pour stocker les satellites
        self.binomes_satellites = []  # Liste des connexions entre les satellites
        self.lignes_connexion = {}  # Dictionnaire pour stocker le binome de satellite et son objet connexion
        self.lignes_antenne = {}  # Dictionnaire pour stocker le couple satellite et son antenne

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
                # Éviter les connexions doubles et les auto-connexions
                for j in range(i + 1, len(self.positions_satellites)):  # Éviter les connexions doubles et les auto-connexions
                    self.binomes_satellites.append((i, j))  # Ajouter chaque couple unique de satellites
                    connexion = ConnexionSatellites((i, j), self.positions_satellites)  # Création de l'objet connexion
                    self.lignes_connexion[(i, j)] = connexion  # Ajout de l'objet connexion dans le dictionnaire

        # Création des objets Antenne
        if self.aff_antenne:  # Si True alors on rentre
            for i in range(len(self.positions_satellites)):  # Ajouter chaque couple unique de satellites
                antenne = Antenne(self.positions_satellites[i])  # Création de l'objet connexion
                self.lignes_antenne[i] = antenne  # Ajout de l'objet connexion dans le dictionnaire

    def initialiser_animation(self):

        # Définition des bornes d'affichage
        max_a = np.max(self.a_satellites)
        max_b = np.max(self.b_satellites)
        self.ax.set_xlim(-max_a - 1000, max_a + 1000)
        self.ax.set_ylim(-max_a - 1000, max_a + 1000)
        self.ax.set_zlim(-max_b - 1000, max_b + 1000)
        self.ax.set_aspect('auto')

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

        # Initialisation animation des antennes
        if self.aff_antenne:
            for i in range(len(self.positions_satellites)):
                line = self.lignes_antenne[i].tracer_cercle_antenne(self.ax, -1)
                artists.append(line)

        # Affichage de la Terre
        if self.aff_terre:
            terre = Terre()
            lines = terre.afficher_terre(self.ax)
            artists.append(lines)

        # Affichage des orbites
        if self.aff_orbite:
            orbites = Orbite(self.positions_satellites)
            lines = orbites.tracer_orbites(self.ax)
            artists.append(lines)
        return artists

    def update_animation(self, n):
        artists = []

        # Mettre à jour les positions des satellites
        for i in range(len(self.positions_satellites)):
            x = self.positions_satellites[i, 0, n]
            y = self.positions_satellites[i, 1, n]
            z = self.positions_satellites[i, 2, n]

            self.satellites[i].set_data([x], [y])
            self.satellites[i].set_3d_properties([z])
            artists.append(self.satellites[i])

            # Mettre à jours toutes les antennes des satellites
            if self.aff_antenne:
                line = self.lignes_antenne[i].tracer_cercle_antenne(self.ax, n)
                artists.append(line)

        # Mettre à jour toutes les lignes de connexion entre les satellites
        if self.aff_connexions:
            for connexion in self.binomes_satellites:
                line = self.lignes_connexion[connexion].mettre_a_jour_connexions(n)
                artists.append(line)

        return artists

    def animate(self):
        anim = animation.FuncAnimation(self.fig, self.update_animation, init_func=self.initialiser_animation,
                                       frames=nb_points, interval=20, blit=True)
        plt.show()
