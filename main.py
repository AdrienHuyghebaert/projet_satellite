# ======================================================================================================================
# Auteurs: Groupe
# Date: 20/06/2024
# Programme: Ce programme permet d'utiliser le module projet_satellite avec toutes ses fonctionnalitées
# ======================================================================================================================

import SatelliteObservation


if __name__ == '__main__':


    # Interface utilisateur

    titre = "Bienvenue dans notre module sur l'étude des orbites des satellites"
    longueur = len(titre) + 4
    print("=" * longueur)
    print(f"| {titre} |")
    print("=" * longueur, '\n')

    liste_parametres = ['Nom_Satellite', 'Numero_NORAD', 'Masse', 'Classe_Orbite', 'Type_Orbite',
                        'Longitude (deg)', 'Perigee (km)', 'Apogee (km)', 'Excentricite', 'Inclinaison (deg)', 'Periode']

    # Choix de l'action a effectuer:
    print("\n\u21D2 Voici les actions possibles de ce programme:\n")
    choix = ["Communication entre deux satellites (0)", "Afficher une constellation de satellites (1)",
             "Affiche la trace d'un satellite sur la Terre (2)",
             "Ajouter les données d'un satellite dans la base de données (3)",
             "Modifier des données d'orbite d'un satellite de la base de données (4)"]
    for item in choix:
        print(f"- {item}")
    choix_action = SatelliteObservation.get_int_input("\n \u21D2 Tapez le numéro de l'action souhaitée: ")

    # Choix des données d'entrées:
    choix_donnees = SatelliteObservation.get_int_input('\u21D2 Souhaitez vous entrer les données de votre satellite (1) ou trouver un satellite dans la base de données (2) ? : \n')

    if choix_action == 0:
        donnees_entree = SatelliteObservation.choisir_format_entree(choix_donnees, 2)

    elif choix_action == 1:
        nbr_satellite = SatelliteObservation.get_int_input('Entrez le nombre de satellite que vous souhaitez afficher (max 5): ')
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

        # Modification de la valeur et affichage de la table modifiee
        nouvelle_valeur = SatelliteObservation.get_int_input('\nQuelle est la nouvelle valeur: ')
        df = objet.modifier_orbite(parametre, numero_NORAD, nouvelle_valeur)
        print('\nVoici la table modifiée: ', df[df['Numero_NORAD'] == numero_NORAD])

    print(SatelliteObservation.choisir_format_entree(1, 2))







'''''Brouillon 
    
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

'''''
