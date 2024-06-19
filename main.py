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

test = SatelliteObservation.Satellite(256, 145, 0.00012, 56, 50)
data = SatelliteObservation.AffichageOrbiteSatellite(1000,
                                                     SatelliteObservation.Satellite.calcul_parametres_ellipse(test)[0],
                                                     SatelliteObservation.Satellite.calcul_parametres_ellipse(test)[1],
                                                     SatelliteObservation.Satellite.calcul_parametres_ellipse(test)[2],
                                                     SatelliteObservation.Satellite.calcul_coord_ellipse_inclinee(test)[
                                                         0],
                                                     SatelliteObservation.Satellite.calcul_coord_ellipse_inclinee(test)[
                                                         1],
                                                     SatelliteObservation.Satellite.calcul_coord_ellipse_inclinee(test)[
                                                         2],
                                                     256, 145, 56, 50)

data.get_data()
data.animate()
