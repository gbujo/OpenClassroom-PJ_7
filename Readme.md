<header>

<!--
  <<< Author notes: Course header >>>
  Include a 1280×640 image, course title in sentence case, and a concise description in emphasis.
  In your repository settings: enable template repository, add your 1280×640 social image, auto delete head branches.
  Add your open source license, GitHub uses MIT license.
-->

</header>

# Projet OpenClassRoom n° 7

## Les sources des 3 projets

Ce repository contient 3 livrables distincts :

- _project dashboard_ : une application pour visualiser les données d'un client et son scoring
- _project entrainement_ : les notebooks d'entrainement des modèles, les analyses de data drift et de feature engineering
- _project predict_ : le modèle sélectionné et une API permettant d'accèder à sa prédiction pour 1 client.

A noter que les répertoires _helloworld_ et _examples_ contiennent des exemples de code donnés à titre illustratif mais qui ne font pas partie des livrables du projet Openclassroom.

## Les workflows d'intégration continue et déployement continu

Le répertoire _.github/workflows_ contient 2 workflows GitHub Actions qui permettent à chaque push des branches _main_ ou _dashboard_ d'effectuer :

- les test unitaires via _pytest_
- le déployement des solutions _Dashboard_ et _API Predict_ sur le Google Cloud via Cloud Run

Les fichiers de configurations sont contenus dans le répertoire des sources de chaque projet, à savoir :

- _requirements.txt_ : liste des dépendances à installer
- _Dockerfile_ : dockerfile pour la construction de l'image du conteneur
- _cloudbuild.yaml_ : fichier d'instruction Google Cloud Platform pour la construction de l'image du conteneur et le déployement


<footer>
N'hésitez pas à me contacter pour toute information complémentaire.
Guillaume