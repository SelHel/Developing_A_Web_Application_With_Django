# Application web permettant à une communauté d'utilisateurs de consulter ou de solliciter des critiques de livres à la demande.
## Descriptif
**LitReview** est une jeune startup qui souhaite développer une nouvelle application web qui permet de demander ou de publier des critiques de livres ou d’articles.<br>
L’application présente deux cas d’utilisation principaux :

* Les personnes qui demandent des critiques sur un livre ou sur un article particulier.
* Les personnes qui recherchent des articles et des livres intéressants à lire, en se basant sur les critiques des autres.

Ma mission était d'intégrer cette application en utilisant le framework Django.<br>
Elle devait répondre aux exigences énoncées dans le cahier des charges, et présenter une structure de base de données équivalente à celle du schéma.<br>
L'interface utilisateur devait correspondre à celle conçue dans les wireframes de l'UX Designer.

## Prérequis
* Python 3.9 ( lien de téléchargement: <https://www.python.org/downloads>)

## Installation de l'application

* Récupérer les livrables du projet sur votre poste de travail en téléchargant le dossier **OpenclassroomsProject9-master** depuis ce lien [GitHub](https://github.com/SelHel/OpenclassroomsProject9.git) ou en clonant le dépôt en utilisant le terminal sous Mac/Linux ou l'invite de commandes sous Windows :<br>

	```
	git clone https://github.com/SelHel/OpenclassroomsProject9.git
	```

* Ensuite, placez vous dans le dossier "OpenclassroomsProject9" et créez un environnement virtuel :

	```
	python -m venv <your-virtual-env-name>
	```

* Activez votre environnement virtuel :

	```
	<your-virtual-env-name>\Scripts\activate.bat (sous Windows)
	```
	ou
	
	```
	source <your-virtual-env-name>/bin/activate (sous Mac/Linux)
	```

* Installer les dépendances avec la commande suivante :

	```
	pip install -r requirements.txt
	```
## Exécution de l'application
* Pour exécuter l'application toujours dans le terminal sous Mac/Linux ou l'invite de commandes sous Windows placez vous dans le dossier "OpenclassroomsProject9" puis exécutez le serveur de développement en utilisant la commande :

	```
	python manage.py runserver
	```

* Pour accéder à la page d'accueil et naviguer dans l'application copier et coller cette adresse dans votre navigateur :
	
	```
	http://127.0.0.1:8000/
	```

## Auteur
**Selim Helaoui**