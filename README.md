# générateur de playlist

Ce projet, comme son nom l'indique, est un générateur de playlist spotify. En se basant sur un artiste choisi par l'utilisateur, le programme va générer une playlist composée de chansons d'artistes similaires à l'artiste choisi afin d'élargir sa culture musicale et découvrir de nouveaux artistes.

## Principe
Il est demandé à l'utilisateur de choisir un artiste sur lequel baser le reste de la playlist. Puis, pour chaque artiste, il lui faudra en choisir 2 semblables, de même pour ces 2 nouveaux artistes, de fil en aiguille, créant une arborescence d'artistes.

Les informations des artistes sont récupérées via l'API Spotify et celle de Lastfm.

### Problème rencontré 
<!-- à mettre dans le rapport plutot -->
Originellement, seulement l'API de Spotify devait être utilisée pour toutes les requêtes. Cependant, en novembre 2024 Spotify a fait quelques changements au niveau de son API, notamment en dépréciant l'endpoint permettant de récuperer des artistes similaires à un artiste donné. Le projet reposant grandement sur cela, il a a fallu trouver une alternative : l'api de Lastfm.


## Avant d'exécuter

### Installation modules

Afin de pouvoir exécuter ce programme correctement, il vous faudra installer les modules/librairies Python nécéssaires (avec *pip install*) :
* requests_cache
* spotipy
* requests
* et graphviz

Pour graphiz, il faut installer les packages sur ce site : https://graphviz.org/download/

Après installation, ajouter à la variable d'environnement PATH le chemin jusqu'au dossier *bin* de graphviz.

**Exemple :** C:\Program Files\Graphviz\bin

*(si le code renvoie une erreur, il faut éventuellement ajouter [chemin]\Graphviz\bin\dot.exe)*

### Utilisation de l'API
1. L'utilisation de l'API Spotify étant limitée pour les applications à petite échelle, il est impossible pour n'importe qui d'exécuter ce code sans encombre.
2. Dans ce contexte d'évaluation, vous ne voulez peut être pas utiliser votre propre compte Spotify pour vous connecter (ou peut être que vous n'en avez pas).

Pour remédier à ces deux problèmes, j'ai créé un compte Spotify que vous pouvez (en réalité, que vous *devez*) utiliser pour utiliser ce code (pour des questions de clé API etc...)
Pour éviter toute erreur, si vous êtes déjà connecté.e à Spotify sur votre navigateur, il faut vous déconnecter.
A la première exécution, il faudra vous connecter avec le compte suivant :

```
adresse mail : projection.lestudio@gmail.com
mot de passe : Algoefficace24
```

Ces login fonctionnent pour le compte Spotify ainsi que le compte Spotify for Developpers associé. (Inutile de s'y connecter)
Les clés API sont créées depuis ce compte et sont déja initialisées dans le fichier `cred.py`, vous n'avez rien à faire.

## Utilisation

### Selection
Au lancement, il faut que l'utilisateur saisisse au clavier le nom de l'artiste sur lequel il veut baser sa playlist. (Ici, pour des raisons d'éfficacité, il vaut mieux saisir un artiste assez populaire afin de ne pas être limité trop rapidement.)

Ce premier artiste est la racine de l'arbre de recommandation.

A  partir de celui-ci, il faut choisir deux autres artistes similaires au premier, qui seront les "enfants" du noeud racine. Une liste de 10 artistes est proposée, il est possible d'en voir plus en tapant `0`.

Ce processus a lieu ensuite pour chaque noeud de l'arbre jusqu'à atteindre le nombre de noeuds souhaités. Un noeud dans l'arbre = une chanson dans la playlist. Il est possible de le modifier dans la variable `nb_max` au debut du code.

### Suppression

> *Non fonctionnelle pour l'instant*

### Visualisation

Une fois tous les noeuds choisis, une visualisation de l'arbre est créée (fichier pdf).

### Création de la playlist

Une fois revenu sur le terminal, un prompt vous demande le nom que vous souhaitez donner à la playlist. Après avoir saisi, l'algorithme va parcourir l'arbre et choisir au hasard une chanson parmi les 10 plus populaires de chaque artiste, et l'ajouter à la playlist.

Enfin, la fonction renvoie le lien de celle-ci, venant d'être ajoutée à votre profil.

