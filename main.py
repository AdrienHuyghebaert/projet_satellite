# ======================================================================================================================
# Auteurs: Groupe 5
# Date: 02/07/2024
# Programme: Ce programme permet d'utiliser le module projet_satellite avec toutes ses fonctionnalitées
# ======================================================================================================================

import SatelliteObservation
import numpy as np


if __name__ == '__main__':


    # Interface utilisateur

    titre = "Bienvenue dans notre module sur l'étude des orbites des satellites"

    SatelliteObservation.afficher_console(titre)

    liste_parametres = ['Nom_Satellite', 'Numero_NORAD', 'Masse', 'Classe_Orbite', 'Type_Orbite',
                        'Longitude (deg)', 'Perigee (km)', 'Apogee (km)', 'Excentricite',
                        'Inclinaison (deg)', 'Periode']

    while True:

        # Choix de l'action a effectuer

        print("\n\u21D2 Voici les actions possibles de ce programme:\n")

        choix = ["Affichage des orbites (1): Communication entre deux satellites et/ou Afficher une constellation de satellites et/ou Affiche la trace d'un satellite sur la Terre",
                 "Ajouter les données d'un satellite dans la base de données (2)",
                 "Modifier des données d'orbite d'un satellite de la base de données (3)", "Quitter le programme (4)"]
        for item in choix:
            print(f"- {item}")
        choix_action = SatelliteObservation.get_int_input("\n \u21D2 Tapez le numéro de l'action souhaitée: ")


        if choix_action == 1:

            # Choix des données d'entrées

            choix_donnees = SatelliteObservation.get_int_input(
                '\n\u21D2 Souhaitez vous entrer les données de votre satellite (YAML) '
                '(1) ou trouver un satellite dans la base de données (2) ? : \n')

            nbr_satellite = SatelliteObservation.get_int_input('\n\u2192 Entrez le nombre de satellite que '
                                                               'vous souhaitez afficher (max 5): \n')
            donnees_entree = SatelliteObservation.choisir_format_entree(choix_donnees, nbr_satellite)

            numeros_norad = []
            donnees_satellites = np.zeros((len(donnees_entree)))
            position_satellites = np.zeros((len(donnees_entree), 3, 1000), dtype=object)

            actions = [0, 0 ,0]
            a_satellites = np.zeros((len(donnees_entree)), dtype=object)
            b_satellites = np.zeros((len(donnees_entree)), dtype=object)
            actions[0] = (SatelliteObservation.get_str_input('\nSouhaitez-vous afficher les connexions (Répondre: True or False)? '))
            actions[1] = (SatelliteObservation.get_str_input('Souhaitez-vous afficher la Terre (Répondre: True or False)? '))
            actions[2] = (SatelliteObservation.get_str_input("Souhaitez-vous afficher l'orbite (Répondre: True or False)? "))

            # Récupération des actions sous forme de booléen
            actions_bool = [SatelliteObservation.str_to_bool(s) for s in actions]

            # On récupère les données pour chaque satellite
            for i in range(len(donnees_entree)):
                satellite = SatelliteObservation.Satellite(donnees_entree[i][0], donnees_entree[i][1], donnees_entree[i][2])
                position_satellites[i] = satellite.calcul_coord_ellipse_inclinee()[3]
                a_satellites[i] = satellite.calcul_parametres_ellipse()[0]
                b_satellites[i] = satellite.calcul_parametres_ellipse()[1]
                numeros_norad.append(donnees_entree[i][3])

            string_numeros_norad = list(map(str, numeros_norad))

            # Affichage des orbites avec les paramètres souhaités

            affichage = SatelliteObservation.AffichageOrbiteTraceConnexion2(position_satellites, a_satellites,
                                                                            b_satellites,
                                                                            actions_bool, string_numeros_norad)
            affichage.animate()


        # Ajout des données d'un satellite dans la base de données (2)

        elif choix_action == 2:

            choix_table = SatelliteObservation.get_str_input(
                '\n\u2192 Avez-vous déjà modifié/ajouté une orbite de satellite '
                '\nSi non un fichier csv nommé Base_donnees_satellites_utilisateur.csv sera créé pour vous '
                '\nRéponse (oui/non): ')

            input("\n\u2192 Pour continuer vous devez renseigner les données de votre satellite dans le fichier deck.yaml "
                  "\nAppuyez sur Entrée lorsque vous avez terminé de modifier le fichier "
                  "\nN'oubliez pas de faire 'ctrl + s' pour sauvegarder les modifications !!...")

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

            print("\nVoici la table modifiée, votre ajout se trouve en dernière ligne:\n\n", df)


        # Modification des données d'un satellite présent dans la base de données (3)

        elif choix_action == 3:

            numero_NORAD = SatelliteObservation.get_int_input(
                '\n\u2192 Entrez le numéro NORAD du satellite à modifier (5 chiffres): ')

            # Affichage de la liste des paramètres orbite et satellite
            print('\nVoici la liste des paramètres:\n ')

            for item in liste_parametres:
                print(f"- {item}")


            parametre = SatelliteObservation.get_str_input('\n\u2192 Quel paramètre souhaitez-vous modifier '
                                                           '(copier-coller le nom dans la liste ci-dessus): ')

            nouvelle_valeur = SatelliteObservation.get_int_input('\n\u2192 Quelle est la nouvelle valeur: ')

            # Instanciation

            choix_table = SatelliteObservation.get_str_input(
                '\n\u2192 Avez-vous déjà modifié/ajouté une orbite de satellite '
                '\nSi non un fichier csv nommé Base_donnees_satellites_utilisateur.csv sera créé pour vous '
                '\nRéponse (oui/non): ')

            if choix_table == 'non':
                table = SatelliteObservation.AjoutOrbite('Entrees/UCS-Satellite-Database 5-1-2023.csv')
                df = table.modifier_orbite(parametre, numero_NORAD, nouvelle_valeur, False)

            elif choix_table == 'oui':
                table = SatelliteObservation.AjoutOrbite('Entrees/Base_donnees_satellites_utilisateur.csv')
                df = table.modifier_orbite(parametre, numero_NORAD, nouvelle_valeur, True)

            # Modification de la valeur et affichage de la table modifiee

            print('\nVoici la table modifiée:\n\n ', df[df['Numero_NORAD'] == numero_NORAD])



        elif choix_action == 4:
            print("\nMerci d'avoir utilisé le programme. Au revoir!")
            break  # Sortir de la boucle et terminer le programme
