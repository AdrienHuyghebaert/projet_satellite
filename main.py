# ======================================================================================================================
# Auteurs: Groupe 5
# Date: 20/06/2024
# Programme: Ce programme permet d'utiliser le module projet_satellite avec toutes ses fonctionnalitées
# ======================================================================================================================

import SatelliteObservation
import numpy as np


if __name__ == '__main__':

    while True:

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
                 "Modifier des données d'orbite d'un satellite de la base de données (3)", "Quitter le programme (4)"]
        for item in choix:
            print(f"- {item}")
        choix_action = SatelliteObservation.get_int_input("\n \u21D2 Tapez le numéro de l'action souhaitée: ")


        if choix_action == 1:

            # Choix des données d'entrées

            choix_donnees = SatelliteObservation.get_int_input(
                '\u21D2 Souhaitez vous entrer les données de votre satellite '
                '(1) ou trouver un satellite dans la base de données (2) ? : \n')

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

            # Affichage des orbites avec les paramètres voulus

            affichage = SatelliteObservation.AffichageOrbiteTraceConnexion2(position_satellites, a_satellites,
                                                                            b_satellites,
                                                                            afficher_connexion, afficher_terre,
                                                                            afficher_orbite)
            affichage.animate()


        # Ajout des données d'un satellite dans la base de données (2)

        elif choix_action == 2:

            choix_table = SatelliteObservation.get_str_input(
                '\nAvez-vous déjà modifié/ajouté une orbite de satellite (oui/non):\n')

            input("\nAppuyez sur Entrée lorsque vous avez terminé de modifier le fichier yaml avec les données du satellite à ajouter...")

            fichier_yaml = SatelliteObservation.Lire_YAML('Entrees/deck.yaml')

            dictionnaire = fichier_yaml.lecture_fichier()
            nouveau_dictionnaire = {
                'SatelliteOrbite': {**dictionnaire.get('Satellite', {}), **dictionnaire.get('Orbite', {})}}

            if choix_table == 'oui':
                nouvelle_data_frame = SatelliteObservation.AjoutOrbite('Entrees/Base_donnees_satellites_utilisateur.csv')
                df = nouvelle_data_frame.ajouter_orbite(nouveau_dictionnaire, True)

            elif choix_table == 'non':
                nouvelle_data_frame = SatelliteObservation.AjoutOrbite('Entrees/UCS-Satellite-Database 5-1-2023.csv')
                df = nouvelle_data_frame.ajouter_orbite(nouveau_dictionnaire, False)

            print("\nVoici la table modifiée, votre ajout se trouve en dernière ligne:\n", df)


        # Modification des données d'un satellite présent dans la base de données (3)

        elif choix_action == 3:

            numero_NORAD = SatelliteObservation.get_int_input(
                '\nEntrez le numéro NORAD du satellite à modifier (5 chiffres): ')

            # Affichage de la liste des paramètres orbite et satellite
            print('\nVoici la liste des paramètres: ')

            for item in liste_parametres:
                print(f"- {item}")
            parametre = SatelliteObservation.get_str_input('\nQuel paramètre souhaitez-vous modifier '
                                                           '(copier-coller le nom dans la liste ci-dessus): ')

            nouvelle_valeur = SatelliteObservation.get_int_input('\nQuelle est la nouvelle valeur: ')

            # Instanciation

            choix_table = SatelliteObservation.get_str_input(
                '\nAvez-vous déjà modifié/ajouté une orbite de satellite (oui/non):\n')

            if choix_table == 'non':
                table = SatelliteObservation.AjoutOrbite('Entrees/UCS-Satellite-Database 5-1-2023.csv')
                df = table.modifier_orbite(parametre, numero_NORAD, nouvelle_valeur, False)

            elif choix_table == 'oui':
                table = SatelliteObservation.AjoutOrbite('Entrees/Base_donnees_satellites_utilisateur.csv')
                df = table.modifier_orbite(parametre, numero_NORAD, nouvelle_valeur, True)

            # Modification de la valeur et affichage de la table modifiee

            print('\nVoici la table modifiée:\n\n ', df[df['Numero_NORAD'] == numero_NORAD])


        elif choix_action == 4:
            print("Merci d'avoir utilisé le programme. Au revoir!")
            break  # Sortir de la boucle et terminer le programme