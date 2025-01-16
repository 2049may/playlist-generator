'''
Arbre de recommandation d'artistes à partir d'une racine définie (choisie ou générée )
nb artistes max : 15-20 (modulable)
par défaut hauteur de 4 : donc 15 artistes

nature des valeurs des noeuds : dictionnaire contenant le nom et l'uri de l'artiste

features :
    * régénérer un noeud si l'artiste proposé ne convient pas
    * générer une playlist basée sur les artistes sélectionnés
    * lire/controller la playlist depuis l'appli/site jsp
        -> lecture aléatoire ?
        -> tris
        -> modifier la playlist (déplacer/supprimer une track)
        -> si noeud supprimé apres-coup, 2 choix :
            * supprimer tout le sous-arbre
            * supprimer seulement le noeud en question. dans ce cas, switch l'artiste supprimé avec une feuille




2 listes :
* artistes selectionnés
* artistes (déja) proposés pour ne pas les re proposer

L'endpoint "Recommandations" de l'api spotify etant deprecated, 
il a fallu trouver un autre moyen pout obtenir des recommandations d'artistes similaires à un artiste donné,
à savoir : passer par l'api de lastfm

utilisation des Files pour la construction de l'arbre de recommandations
'''

'''
logs :
projet fonctionnel overall, reste la gestion d'erreurs, ne pas mettre le meme artiste 2 fois, et la creation de la playlist, la suppression et
regeneration de noeuds
tester si ça fonctionne avec un autre compte ptdrrrrr

installer graphviz et les autres dépendances. si besoin (si erreur) préciser le PATH dans la variable correspondante. 

'''