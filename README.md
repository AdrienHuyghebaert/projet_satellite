# projet_satellite
Projet final du cours MGA802 de l'ETS

**Objectifs :** 

Tracer l'orbite de plusieurs satellites ainsi que :
- la trace de leur antenne au sol
- la potentielle connection entre 2 satellites

Tout cela est fait à partir données d'orbites fournis par l'utilisateur ou à partir d'une base de données déjà présente dans le Git. 

**Modules nécessaires :**

- *numpy*
- *matplotlib.pyplot*
- *matplotlib.animation*
- *PyYAML*
- *pandas*

**Fonctionnement :**

Le code s'appuit sur une structure en class. 

Tous les appels sont fait à partir du main. Nous allons dans les parties suivantes décrire le fonctionnement de chacunes des classes et leurs méthodes.

Les fonctionnalités principales du code sont :
- Affichage : permet d'afficher les satellites, leur orbite, le lien de connection, la marque de leur antenne au sol.
- Données d'entrées : permet au choix de récupérer les données d'entrées à partir d'un fichier YAML fournis par l'utilisateur, de prendre des données dans une base de donnée CSV, écrire les informations du fichier YAML vers le CSV
- Satellite : calcul les points d'orbites à partir des paramètres d'orbite

Comme une image est toujours plus explicite voici les fonctionnalitées implémentées :

- Tracer les orbites :

![image](https://github.com/AdrienHuyghebaert/projet_satellite/assets/169941933/2c36d94a-67cf-48fd-8573-62281c75af78)

- Montrer la connection entre les satellites :

![image](https://github.com/AdrienHuyghebaert/projet_satellite/assets/169941933/b2c0d9b1-d3e5-4c14-a83c-af15794c5532)

- Afficher la marque de l'antenne du satellite sur la Terre :

![image](https://github.com/AdrienHuyghebaert/projet_satellite/assets/169941933/cb1d38ac-24db-4362-b99e-c9965fc6975c)

