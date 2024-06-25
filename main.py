# ======================================================================================================================
# Auteurs: Groupe
# Date: 20/06/2024
# Programme: Ce programme permet d'utiliser le module projet_satellite avec toutes ses fonctionnalitées
# ======================================================================================================================

import SatelliteObservation


if __name__ == '__main__':

    '''Interface utilisateur'''

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
    choix = ["Communication entre deux satellites (0)", "Afficher une constellation de satellites (1)",
             "Affiche la trace d'un satellite sur la Terre (2)",
             "Ajouter les données d'un satellite dans la base de données (3)",
             "Modifier des données d'orbite d'un satellite de la base de données (4)"]
    for item in choix:
        print(f"- {item}")
    choix_action = SatelliteObservation.get_int_input("\n \u21D2 Tapez le numéro de l'action souhaitée: ")

    # Choix des données d'entrées

    choix_donnees = SatelliteObservation.get_int_input('\u21D2 Souhaitez vous entrer les données de votre satellite '
                                                       '(1) ou trouver un satellite dans la base de données (2) ? : \n')

    if choix_action == 0:
        donnees_entree = SatelliteObservation.choisir_format_entree(choix_donnees, 2)

    elif choix_action == 1:
        nbr_satellite = SatelliteObservation.get_int_input('Entrez le nombre de satellite que '
                                                           'vous souhaitez afficher (max 5): ')
        donnees_entree = SatelliteObservation.choisir_format_entree(choix_donnees, nbr_satellite)


    elif choix_action == 2:
        donnees_entree = SatelliteObservation.choisir_format_entree(choix_donnees, 1)


    # Ajout des données d'un satellite dans la base de données (3)


    elif choix_action == 3:
        objet = SatelliteObservation.Lire_YAML('Entrees/deck.yaml')
        dictionnaire = objet.lecture_fichier()
        nouveau_dictionnaire = {
            'SatelliteOrbite': {**dictionnaire.get('Satellite', {}), **dictionnaire.get('Orbite', {})}}
        print(nouveau_dictionnaire)
        nouvelle_data_frame = SatelliteObservation.AjoutOrbite('Entrees/UCS-Satellite-Database 5-1-2023.csv')
        df = nouvelle_data_frame.ajouter_orbite(nouveau_dictionnaire)
        print(df)

    # Modification des données d'un satellite présent dans la base de données (4)

    elif choix_action == 4:
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










'''''Brouillon 
    
=======
    '''''

    float = SatelliteObservation.get_float_input('Entrez un float : \n')
    print(float)
    entier = SatelliteObservation.get_int_input('Entrez un entier : \n')
    print(entier)
    str = SatelliteObservation.get_str_input('Entrez un str : \n')
    print(str)

    satellite = SatelliteObservation.Satellite(256, 145, 0.00012, 56, 50)

    satellite.tracer_orbite_3d()

    

# Test ajout base de données panda et enregistrement fichier csv
objet = SatelliteObservation.Lire_YAML('Entrees/deck.yaml')
dictionnaire = objet.lecture_fichier()
nouveau_dictionnaire = {'SatelliteOrbite': {**dictionnaire.get('Satellite', {}), **dictionnaire.get('Orbite', {})}}
print(nouveau_dictionnaire)
nouvelle_data_frame = SatelliteObservation.AjoutOrbite('Entrees/UCS-Satellite-Database 5-1-2023.csv')
df = nouvelle_data_frame.ajouter_orbite(nouveau_dictionnaire)
print(df)

# Test modification d'une orbite
objet2 = SatelliteObservation.AjoutOrbite('Entrees/UCS-Satellite-Database 5-1-2023.csv')
df = objet2.modifier_orbite('Masse', 55107, 45)
print(df[df['Numero_NORAD'] == 55107])


# numero_NORAD = 25631
# base = SatelliteObservation.AjoutOrbite('Entrees/UCS-Satellite-Database 5-1-2023.csv', dictionnaire)
# print(base.lire_base_donnees())

# nouvelle_data_frame = SatelliteObservation.AjoutOrbite('Entrees/UCS-Satellite-Database 5-1-2023.csv', dictionnaire)
# print(nouvelle_data_frame.ajouter_orbite())
# nouvelle_data_frame.enregistrer_nouvelle_base_donnees()




satellite_1 = SatelliteObservation.Satellite(10, 10500, 0.9, 5, 50)
satellite_2 = SatelliteObservation.Satellite(30006, 6, 0.8, 36.9, 40)
satellite_3 = SatelliteObservation.Satellite(956, 897, 0.7, 90, 4000)
satellite_4 = SatelliteObservation.Satellite(720, 12, 0.7, 12, 12)
'''
afficher_orbite = SatelliteObservation.AffichageOrbiteSatellite(1000,
                                                                SatelliteObservation.Satellite.calcul_parametres_ellipse
                                                                (satellite_1)[0],
                                                                SatelliteObservation.Satellite.calcul_parametres_ellipse
                                                                (satellite_1)[1],
                                                                SatelliteObservation.Satellite.
                                                                calcul_coord_ellipse_inclinee(
                                                                    satellite_1)[0],
                                                                SatelliteObservation.Satellite.
                                                                calcul_coord_ellipse_inclinee(
                                                                    satellite_1)[1],
                                                                SatelliteObservation.Satellite.
                                                                calcul_coord_ellipse_inclinee(
                                                                    satellite_1)[2])

afficher_orbite.get_data()
afficher_orbite.animate()
'''
# Affichage de plusieurs orbites
a_sat_1 = SatelliteObservation.Satellite.calcul_parametres_ellipse(satellite_1)[0]
a_sat_2 = SatelliteObservation.Satellite.calcul_parametres_ellipse(satellite_2)[0]
a_sat_3 = SatelliteObservation.Satellite.calcul_parametres_ellipse(satellite_3)[0]
a_sat_4 = SatelliteObservation.Satellite.calcul_parametres_ellipse(satellite_4)[0]
a_satellites = np.array([a_sat_1, a_sat_2, a_sat_3, a_sat_4])

b_sat_1 = SatelliteObservation.Satellite.calcul_parametres_ellipse(satellite_1)[1]
b_sat_2 = SatelliteObservation.Satellite.calcul_parametres_ellipse(satellite_2)[1]
b_sat_3 = SatelliteObservation.Satellite.calcul_parametres_ellipse(satellite_3)[1]
b_sat_4 = SatelliteObservation.Satellite.calcul_parametres_ellipse(satellite_4)[1]
b_satellites = np.array([b_sat_1, b_sat_2, b_sat_3, b_sat_4])

positions_sat_1 = SatelliteObservation.Satellite.calcul_coord_ellipse_inclinee(satellite_1)[3]
positions_sat_2 = SatelliteObservation.Satellite.calcul_coord_ellipse_inclinee(satellite_2)[3]
positions_sat_3 = SatelliteObservation.Satellite.calcul_coord_ellipse_inclinee(satellite_3)[3]
positions_sat_4 = SatelliteObservation.Satellite.calcul_coord_ellipse_inclinee(satellite_4)[3]
positions_satellites = np.array([positions_sat_1, positions_sat_2, positions_sat_3, positions_sat_4])

# Paramètre qui permet d'afficher ou non les connexions entre les satellites
afficher_connexions = True
afficher_terre = True
afficher_orbite = True
print(positions_satellites)
affichage = SatelliteObservation.AffichageOrbiteTraceConnexion2(positions_satellites, a_satellites, b_satellites,
                                                                afficher_connexions, afficher_terre, afficher_orbite)
affichage.animate()

'''
# Test de la class TraceAntenne
'''
# test = SatelliteObservation.Satellite(256, 145, 0.00012, 56, 50)
# x_pos, y_pos, z_pos = SatelliteObservation.Satellite.calcul_coord_ellipse_inclinee(test)
# position_sat = [x_pos[567], y_pos[567], z_pos[567]]
# data = SatelliteObservation.TraceAntenne(position_sat)
# data.tracer_cercle()

