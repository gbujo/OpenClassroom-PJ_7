<header>

<!--
  <<< Author notes: Course header >>>
  Include a 1280×640 image, course title in sentence case, and a concise description in emphasis.
  In your repository settings: enable template repository, add your 1280×640 social image, auto delete head branches.
  Add your open source license, GitHub uses MIT license.
-->

</header>

# Projet OpenClassRoom n° 7

## Les objectifs du projet

Extraits de [OpenClassroom](https://openclassrooms.com/fr/paths/164/projects/632/assignment) :

Vous êtes Data Scientist au sein d'une société financière, nommée "Prêt à dépenser", qui propose des crédits à la consommation pour des personnes ayant peu ou pas du tout d'historique de prêt.

 
L’entreprise souhaite mettre en œuvre un outil de “scoring crédit” pour calculer la probabilité qu’un client rembourse son crédit, puis classifie la demande en crédit accordé ou refusé. Elle souhaite donc développer un algorithme de classification en s’appuyant sur des sources de données variées (données comportementales, données provenant d'autres institutions financières, etc.).

De plus, les chargés de relation client ont fait remonter le fait que les clients sont de plus en plus demandeurs de transparence vis-à-vis des décisions d’octroi de crédit. Cette demande de transparence des clients va tout à fait dans le sens des valeurs que l’entreprise veut incarner.
Prêt à dépenser décide donc de développer un dashboard interactif pour que les chargés de relation client puissent à la fois expliquer de façon la plus transparente possible les décisions d’octroi de crédit, mais également permettre à leurs clients de disposer de leurs informations personnelles et de les explorer facilement. 


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

N'hésitez pas à me contacter pour toute information complémentaire.
Guillaume
<footer>
</footer>
