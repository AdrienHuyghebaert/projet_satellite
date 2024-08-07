# Projet_Satellite
### Projet final du cours MGA802 de l'ETS ###

Auteurs: *ADRIEN HUYGHEBAERT - BAPTISTE ROUANET - CLELIA DURANDET*

## Objectifs :

Tracer l'orbite de plusieurs satellites ainsi que :
- la trace de leur antenne au sol
- la potentielle connexion entre 2 satellites
- mettre à jour la base de données

Tout cela est fait à partir d'une base de données déjà présente dans le dépôt Git: UCS-Satellite-Database 5-1-2023.csv

## Modules nécessaires :

- *numpy*
- *matplotlib.pyplot*
- *matplotlib.animation*
- *PyYAML*
- *pandas*

## Fonctionnement :

Le code s'appuit sur une structure en *class*. 

Tous les appels sont fait à partir du main. Nous allons dans les parties suivantes décrire le fonctionnement de chacunes des classes et leurs méthodes.

Les fonctionnalités principales du code sont :
- Affichage : permet d'afficher les satellites, leur orbite, le lien de connexion, la marque de leur antenne au sol.
- Données d'entrées : permet au choix de récupérer les données d'entrées à partir d'un fichier YAML fournis par l'utilisateur, de prendre des données dans une base de donnée CSV, écrire les informations du fichier YAML vers le CSV
- Satellite : calcul les points d'orbites à partir des paramètres d'orbite

Comme une image est toujours plus explicite voici les fonctionnalitées implémentées :

- Tracer les orbites :

![image](https://github.com/AdrienHuyghebaert/projet_satellite/assets/169941933/2c36d94a-67cf-48fd-8573-62281c75af78)

- Montrer la connexion entre les satellites :

![image](https://github.com/AdrienHuyghebaert/projet_satellite/assets/169941933/b2c0d9b1-d3e5-4c14-a83c-af15794c5532)

- Afficher la marque de l'antenne du satellite sur la Terre :

![image](https://github.com/AdrienHuyghebaert/projet_satellite/assets/169941933/cb1d38ac-24db-4362-b99e-c9965fc6975c)

**Données d'entrée**
- fichier deck.yaml
    - données satellite en vrac
    - données TLE (2 lignes)
- base de données fournie: https://www.ucsusa.org/resources/satellite-database

**Données de sortie**
- fichier csv de base de données
- graphique: orbites des satellites + terre + connexions + zone antenne + légende
- affichage console: tableau panda des données des satellites à afficher

**Source pour les calculs de mécanique orbitale**

![image](https://github.com/AdrienHuyghebaert/projet_satellite/assets/169942081/c33fb0a5-d0d1-4d3d-b95a-eebcd47516c4)


### Structure du code

Le code contient les 4 packages et les classes suivants:

- ***DonneesEntree***
  - ajouter_mettre_a_jour_orbite: permet à l'utilisateur d'ajouter les données d'une orbite de satellite dans la base de données ou de modifier les données d'un satellite déjà dans la base
  - base_donnee: permet d'extraire les données d'orbite d'un satellite selon son numéro d'identification NORAD
  - fichier_YAML: permet de récupérer les données du fichier YAML et de les extraire pour leur utilisation
  - lecteur_YAML: permet de lire le fichier YAML
- ***Satellite***
    - satellite: effectue les calculs des paramètres de l'orbite elliptique à partir des données brutes de la base de données
- ***ExtraFunctions***
    - choix_donnees_entree: fonction qui permet de renvoyer des tableaux de données des satellites selon le type de données d'entrée choisie par l'utilisateur 
    - get_user_input: fonction qui permet de récupérer les entrées de l'utilisateur dans la console selon le type (str, int, float)
    - affichage_console: pour l'affichage des titres dans la console utilisateur
- ***Affichage***
    - affichage: permet de gérer tout l'affichage et l'animation des satellites, des orbites, des connexions, des traces et de la Terre
    - terre: classe qui est appelée par affichage (si l'utilisateur souhaite l'afficher) et retourne des lignes 3D formant la Terre
    - orbite: classe qui est appelée par affichage (si l'utilisateur souhaite les afficher), qui calcul les orbites pour des satellites et retourne les lignes 3D correspondantes
    - connexions_satellites: classe qui est appelée par affichage (si l'utilisateur souhaite les afficher), qui détermine si il y a une communication possible entre les satellites et retourne une ligne 3D entre ces 2 derniers si la condition est remplie
    - antenne: classe qui est appelée par affichage (si l'utilisateur souhaite les afficher), qui calcul le cone de vision du satellite et retourne une ligne 3D qui correspond à la trace de ce cone sur la Terre



## Utilisation du code

Pour utiliser le programme, l'utilisateur doit lancer le *main*. Toutes les instructions seront affichées dans la console.

L'utilisateur peut choisir entre différentes ***actions*** possibles:
- Affichage des orbites (1): Communication entre deux satellites et/ou Afficher une constellation de satellites et/ou Affiche la zone accessible par l'antenne sur la Terre
- Ajouter les données d'un satellite dans la base de données (2)
- Modifier des données d'orbite d'un satellite de la base de données (3)
- Quitter le programme (4)

Pour l'action **(1)** l'utilisateur aura:

***2 choix pour les données d'entrée:***
- Trouver des satellites dans la base de données csv à partir du numéro NORAD (Le Satellite Catalog Number ou identifiant NORAD est un identifiant à 5 chiffres assigné par les autorités militaires américaines à tout objet placé en orbite autour de la Terre)
- Rentrer lui-même les paramètres d'un satellite dans le fichier YAML ou les données TLE dans le fichier YAML

***4 choix d'affichage:***
- Par défaut le script affiche tout (orbites, connexionns entre satellites, antennes et Terre) mais il peut personnaliser à l'aide de True or False ce qu'il souhaite afficher.

L'affichage est limité à 5 satellites par souci de temps d'affichage lié au module *animate* mais techniquement un nombre n de satellites peut être sélectionné.

Pour les actions **(2)** et **(3)**, l'utilisateur devra rentrer les données du satellite à ajouter/modifier dans le fichier *deck.yaml*.

Si c'est la première fois qu'il réalise l'une ou l'autre des deux opérations, un fichier csv sera créé dans le dossier *Entrées* afin de garder la base de données intacte. 
A la suite, s'il réalise à nouveau les actions (2) ou (3), les modifications seront ajoutées au fichier csv créé pour l'utilisateur.

