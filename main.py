# ======================================================================================================================
# Auteurs: Groupe 5
# Date: 20/06/2024
# Programme: Ce programme permet d'utiliser le module projet_satellite avec toutes ses fonctionnalitées
# ======================================================================================================================

import SatelliteObservation
import numpy as np


if __name__ == '__main__':

    # Interface utilisateur

    titre = "Bienvenue dans notre module sur l'étude des orbites des satellites"
    longueur = len(titre) + 4
    print("=" * longueur)
    print(f"| {titre} |")
    print("=" * longueur, '\n')

    liste_parametres = ['Nom_Satellite', 'Numero_NORAD', 'Masse', 'Classe_Orbite', 'Type_Orbite',
                        'Longitude (deg)', 'Perigee (km)', 'Apogee (km)', 'Excentricite',
                        'Inclinaison (deg)', 'Periode']

    # Choix de l'action a effectuer

    print("\n\u21D2 Voici les actions possibles de ce programme:\n")
    choix = ["Affichage des orbites (1): Communication entre deux satellites ou Afficher une constellation de satellites ou Affiche la trace d'un satellite sur la Terre",
             "Ajouter les données d'un satellite dans la base de données (2)",
             "Modifier des données d'orbite d'un satellite de la base de données (3)"]
    for item in choix:
        print(f"- {item}")
    choix_action = SatelliteObservation.get_int_input("\n \u21D2 Tapez le numéro de l'action souhaitée: ")

    # Choix des données d'entrées

    choix_donnees = SatelliteObservation.get_int_input('\u21D2 Souhaitez vous entrer les données de votre satellite '
                                                       '(1) ou trouver un satellite dans la base de données (2) ? : \n')

    if choix_action == 1:
        nbr_satellite = SatelliteObservation.get_int_input('Entrez le nombre de satellite que '
                                                           'vous souhaitez afficher (max 5): ')
        donnees_entree = SatelliteObservation.choisir_format_entree(choix_donnees, nbr_satellite)
        print(type(donnees_entree[0][1]))

        donnees_satellites = np.zeros((len(donnees_entree)))
        position_satellites = np.zeros((len(donnees_entree), 3, 1000), dtype=object)

        a_satellites = np.zeros((len(donnees_entree)), dtype=object)
        b_satellites = np.zeros((len(donnees_entree)), dtype=object)
        afficher_connexion = SatelliteObservation.get_str_input('Souhaitez-vous afficher les connexions (Répondre: True or False)?')
        afficher_terre = SatelliteObservation.get_str_input('Souhaitez-vous afficher la Terre (Répondre: True or False)?')
        afficher_orbite = SatelliteObservation.get_str_input("Souhaitez-vous afficher l'orbite (Répondre: True or False)?")

        for i in range(len(donnees_entree)):
            satellite = SatelliteObservation.Satellite(donnees_entree[i][0], donnees_entree[i][1], donnees_entree[i][2])
            position_satellites[i] = satellite.calcul_coord_ellipse_inclinee()[3]
            a_satellites[i] = satellite.calcul_parametres_ellipse()[0]
            b_satellites[i] = satellite.calcul_parametres_ellipse()[1]
        SatelliteObservation.AffichageOrbiteTraceConnexion2(position_satellites, a_satellites, b_satellites, afficher_connexion, afficher_terre, afficher_orbite)

        affichage = SatelliteObservation.AffichageOrbiteTraceConnexion2(position_satellites, a_satellites,
                                                                        b_satellites,
                                                                        afficher_connexion, afficher_terre,
                                                                        afficher_orbite)
        affichage.animate()


    # Ajout des données d'un satellite dans la base de données (2)

    elif choix_action == 2:
        donnees_entree = SatelliteObservation.choisir_format_entree(choix_donnees, 1)
        dictionnaire = donnees_entree.lecture_fichier()
        nouveau_dictionnaire = {
            'SatelliteOrbite': {**dictionnaire.get('Satellite', {}), **dictionnaire.get('Orbite', {})}}
        nouvelle_data_frame = SatelliteObservation.AjoutOrbite('Entrees/UCS-Satellite-Database 5-1-2023.csv')
        df = nouvelle_data_frame.ajouter_orbite(nouveau_dictionnaire)
        print(df)

    # Modification des données d'un satellite présent dans la base de données (3)

    elif choix_action == 3:
        # Instanciation
        objet = SatelliteObservation.AjoutOrbite('Entrees/UCS-Satellite-Database 5-1-2023.csv')
        numero_NORAD = SatelliteObservation.get_int_input('Entrez le numéro NORAD du satellite à modifier (5 chiffres): ')

        # Affichage de la liste des paramètres orbite et satellite
        print('\nVoici la liste des paramètres: ')
        for item in liste_parametres:
            print(f"- {item}")
        parametre = SatelliteObservation.get_str_input('\nQuel paramètre souhaitez-vous modifier: ')

    print('=' * 30, "Bienvenue dans notre module sur l'étude des orbites des satellites", '=' * 30, '\n')
    choix_donnees = SatelliteObservation.get_int_input(
        'Souhaitez vous entrer les données de votre satellite (1) ou trouver un satellite dans la base de données (2) '
        '? : \n')

    # Entrée: fichier YAML
    if choix_donnees == 1:
        print('Veuillez renseigner les données dans le fichier deck.yaml avant de poursuivre')
        choix_yaml = (SatelliteObservation.get_int_input
                      ('Voulez vous utiliser les données satellite (tapez 0) ou bien les données TLE (tapez 1): \n'))

        # Entrée YAML: données satellite
        if choix_yaml == 0:
            fichier_yaml = SatelliteObservation.Lire_YAML('Entrees/deck.yaml')  # instanciation objet
            donnees = fichier_yaml.donnees_satellite()
            print(donnees[0])

        # Entrée YAML: TLE
        elif choix_donnees == 1:
            fichier_yaml_TLE = SatelliteObservation.Lire_YAML('Entrees/deck.yaml')  # instanciation objet
            donnees = fichier_yaml_TLE.donnees_TLE()
            print(donnees)


        # Modification de la valeur et affichage de la table modifiee
        nouvelle_valeur = SatelliteObservation.get_int_input('\nQuelle est la nouvelle valeur: ')
        df = objet.modifier_orbite(parametre, numero_NORAD, nouvelle_valeur)
        print('\nVoici la table modifiée: ', df[df['Numero_NORAD'] == numero_NORAD])
