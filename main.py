import SatelliteObservation
import numpy as np

if __name__ == '__main__':

    # Interface utilisateur

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

    # Entrée: Base de données (fichier csv)
    elif choix_donnees == 2:
        numero_NORAD = SatelliteObservation.get_int_input('Entrez le numéro NORAD du satellite à étudier:')
        base = SatelliteObservation.BaseDonnees('Entrees/UCS-Satellite-Database 5-1-2023.csv', numero_NORAD)
        print(base.appel_base_donnees())

    '''''
    float = SatelliteObservation.get_float_input('Entrez un float : \n')
    print(float)
    entier = SatelliteObservation.get_int_input('Entrez un entier : \n')
    print(entier)
    str = SatelliteObservation.get_str_input('Entrez un str : \n')
    print(str)

    satellite = SatelliteObservation.Satellite(256, 145, 0.00012, 56, 50)

    satellite.tracer_orbite_3d()
   '''''

satellite_1 = SatelliteObservation.Satellite(10, 10500, 0.9, 5, 50)
satellite_2 = SatelliteObservation.Satellite(30006, 6, 0.8, 36.9, 40)
satellite_3 = SatelliteObservation.Satellite(956, 897, 0.7, 90, 4000)
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
a_satellites = np.array([a_sat_1, a_sat_2, a_sat_3])

b_sat_1 = SatelliteObservation.Satellite.calcul_parametres_ellipse(satellite_1)[1]
b_sat_2 = SatelliteObservation.Satellite.calcul_parametres_ellipse(satellite_2)[1]
b_sat_3 = SatelliteObservation.Satellite.calcul_parametres_ellipse(satellite_3)[1]
b_satellites = np.array([b_sat_1, b_sat_2, b_sat_3])

positions_sat_1 = SatelliteObservation.Satellite.calcul_coord_ellipse_inclinee(satellite_1)[3]
positions_sat_2 = SatelliteObservation.Satellite.calcul_coord_ellipse_inclinee(satellite_2)[3]
positions_sat_3 = SatelliteObservation.Satellite.calcul_coord_ellipse_inclinee(satellite_3)[3]
positions_satellites = np.array([positions_sat_1, positions_sat_2, positions_sat_3])

# Paramètre qui permet d'afficher ou non les connexions entre les satellites
afficher_connexions = True
afficher_terre = True

affichage = SatelliteObservation.AffichageOrbiteTraceConnection2(positions_satellites, a_satellites, b_satellites,
                                                                afficher_connexions, afficher_terre)
affichage.animate()

'''
# Test de la class TraceAntenne
'''
# test = SatelliteObservation.Satellite(256, 145, 0.00012, 56, 50)
# x_pos, y_pos, z_pos = SatelliteObservation.Satellite.calcul_coord_ellipse_inclinee(test)
# position_sat = [x_pos[567], y_pos[567], z_pos[567]]
# data = SatelliteObservation.TraceAntenne(position_sat)
# data.tracer_cercle()
