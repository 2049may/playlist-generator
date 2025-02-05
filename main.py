# imports généraux
from Arbre import Noeud
import os
import lastfm
import requests_cache
import File
import graphviz
import cred
import random
import time


# erreur de path (de mon côté), donc ajout du path de graphviz manuellement, ligne à commenter s'il n'y à pas de'erreur.
# sinon, ajouter le path de graphviz manuellement dans la ligne suivante
# os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

requests_cache.install_cache() # pour éviter de refaire les requêtes

# imports spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# authentification
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.SPOTIFY_CLIENT_ID,
                                               client_secret=cred.SPOTIFY_CLIENT_SECRET,
                                               redirect_uri="http://127.0.0.1:9090",
                                               scope="user-library-read playlist-modify-public playlist-modify-private"))

def main() :
    global root
    global nom_playlist
    '''
    Fonction principale
    '''
    
    query = input("Sur quel artiste voulez-vous baser votre playlist ? ")

    nb_max = 7 # nombre maximum d'artistes dans l'arbre = nombre de chansons dans la playlist (+- 1)
    result_type = "artist" # type de résultat recherché

    results = sp.search(q=query, type=result_type, limit=5)  # requête à l'API Spotify

    # affichage des résultats
    print(f"Résultats pour {query} :")
    k = 1
    for artist in results['artists']['items']:
        if artist['genres']:
            genres = f"Genres: {', '.join(artist['genres'])}"
        else:
            genres = "Genres: Unknown"
        print(f"\t{k} - {artist['name']}, {genres}")
        k += 1
        print()

    # choix de l'artiste racine
    choix = -1
    while choix < 0 or choix >= len(results['artists']['items']):    
        try :
            choix = int(input("Choisissez l'artiste que vous recherchez (saisir son numéro) : "))-1
            if choix < 0 or choix >= len(results['artists']['items']):
                raise ValueError("Invalid artist number")
        except ValueError:
            print("Veuillez entrer un nombre valide.")
        print()

    print(f"Vous avez choisi {results['artists']['items'][choix]['name']}")
    print()
    print("=============================================================")
    time.sleep(1)

    # on definit la racine de l'arbre
    root_name = results['artists']['items'][choix]['name']
    root_uri = results['artists']['items'][choix]['uri']

    root = Noeud({"name": root_name, "uri": root_uri}) # dict contenant le nom et l'uri de l'artiste

    # on construit l'arbre de recommandations
    construire_arbre(root, nb_max)
    
    # affichage de l'arbre avec graphviz
    display_tree_graphviz(root)

    nom_playlist = input("Entrez le nom de la playlist (0 pour mettre un nom par défaut): ") 
    if nom_playlist == "0":
        nom_playlist = root.valeur['name'] + " playlist"
        
    create_playlist(nom_playlist)


def construire_arbre(noeud, nb_max):
    '''
    noeud : noeud racine de l'arbre au premier appel, puis noeud courant à chaque appel récursif
    nb_noeuds : nombre de noeuds courants
    nb_max : nombre de noeuds maximum (15 par défaut)
    construit l'arbre de recommandations à partir de l'artiste racine, arbre construit de manière récursive en largeur
    '''
    global artistes_choisis

    nb_noeuds = 1

    file = File.File() # file pour le parcours en largeur
    file.enfiler((noeud, 1)) # chaque élément de la file est un tuple (noeud, niveau)
    artistes_choisis = [root.valeur['name']]
    niveau = 0

    while not file.est_vide() and nb_noeuds <= nb_max:
        noeud, niveau = file.defiler()

        if niveau >= 4:
            continue

        json_artistes = lastfm.get_similar_artists(noeud.valeur['name'], artistes_choisis)

        if json_artistes['similarartists']['artist'] == []:
            print("Impossible de trouver des artistes similaires pour " + noeud.valeur['name'])
            time.sleep(1)
            print()
            continue  # la branche s'arrête si on ne trouve pas d'artistes similaires

        nb_noeuds = process_artists(noeud, json_artistes, nb_noeuds, file, niveau)

    return nb_noeuds


def process_artists(noeud, json_artistes, nb_noeuds, file, niveau, debut=0):
    '''
    noeud : noeud courant
    json_artistes : liste des artistes similaires format json
    nb_noeuds : nombre de noeuds courants
    file : file pour le parcours en largeur
    niveau : niveau du noeud courant
    return : nombre de noeuds après traitement
    cette fonction gère le choix des artistes à garder dans l'arbre et les ajoute au noeud courant
    '''
    debut = 0
    choisi = False

    print("Artiste : " + noeud.valeur['name'])
    print()

    while not choisi:
        lastfm.print_similar_artists(json_artistes, debut, debut + 10)
        print()
        choix = input("Veuillez selectionner deux artistes que vous souhaitez conserver (taper les deux numéros séparés d'un espace \n0 pour voir d'autres artistes) : ")
        print()

        if choix == "0":
            debut += 10
            if debut >= 30:
                print("Vous avez atteint la fin de la liste.")
                print()
                debut = 0
            continue

        fg, fd = valider_choix(choix, json_artistes, debut)
        if fg is None or fd is None:
            continue

        nom_gauche = json_artistes['similarartists']['artist'][fg]['name']
        nom_droit = json_artistes['similarartists']['artist'][fd]['name']

        print("Vous avez choisi : " + nom_gauche + " et " + nom_droit)
        print()

        time.sleep(0.5)

        artistes_choisis.append(nom_gauche)
        artistes_choisis.append(nom_droit)

        print_artistes_choisis()

        artiste_gauche = get_artist_by_name(nom_gauche)
        artiste_droit = get_artist_by_name(nom_droit)

        artiste_gauche = gerer_artiste_nul(artiste_gauche, nom_gauche, json_artistes, debut)
        artiste_droit = gerer_artiste_nul(artiste_droit, nom_droit, json_artistes, debut)

        fg_node = Noeud({'name': artiste_gauche['name'], 'uri': artiste_gauche['uri']})
        fd_node = Noeud({'name': artiste_droit['name'], 'uri': artiste_droit['uri']})

        noeud.gauche = fg_node
        noeud.droit = fd_node

        nb_noeuds = root.taille()
        choisi = True

        print()
        os.system('cls')

        # TODO : ici, suppression d'un artiste (non fonctionnel, code disponible dans backup.py)


        file.enfiler((fg_node, niveau + 1))
        file.enfiler((fd_node, niveau + 1))

        print("=============================================================")
        # print("nb noeuds : ", nb_noeuds)

    return nb_noeuds


def valider_choix(choix, json_artistes, debut):
    '''
    choix : entier, choix de l'utilisateur
    json_artistes : liste des artistes similaires format json
    return : fg, fd, indices des artistes choisis
    gestion d'erreur de saisie
    '''
    try:
        fg, fd = choix.split(" ")
        if len(fg) == 0 or len(fd) == 0:
            raise ValueError("Veuillez entrer deux nombres.")
        fg, fd = int(fg) - 1, int(fd) - 1

        if fg < 0 or fd < 0 or fg >= debut+10 or fd >= debut + 10:
            raise ValueError("Veuillez entrer des nombres valides.")

        return fg, fd

    except ValueError:
        print("==============================================================================")
        print("Entrée invalide. Veuillez entrer deux numéros valides séparés par un espace.")
        print()
        return None, None
    except Exception:
        print("==============================================================================")
        print("Entrée invalide. Veuillez entrer exactement deux numéros séparés par un espace.")
        return None, None


def gerer_artiste_nul(artiste, nom, json_artistes, debut):
    '''
    artiste : artiste à gérer
    nom : nom de l'artiste
    json_artistes : liste des artistes similaires format json
    debut : index de début de la liste
    return : artiste choisi
    Propose à l'utilisateur de choisir un autre artiste si l'artiste est nul
    '''
    while artiste is None: #si l'artiste n'est pas nul, on n'entre pas dans la boucle donc complexité O(1)
        artistes_choisis.remove(nom)
        print("Impossible de trouver l'artiste " + nom)
        lastfm.print_similar_artists(json_artistes, debut=0, fin=15)

        try:
            choix = input("Veuillez choisir un autre artiste : ")
            print()

            if len(choix.split()) != 1:
                raise ValueError("Veuillez entrer un seul nombre.")

            choix = int(choix)
            nom = json_artistes['similarartists']['artist'][int(choix) - 1]['name']
            artiste = get_artist_by_name(nom)

            print("Vous avez choisi : " + nom)
            time.sleep(2)

            artistes_choisis.append(nom)

            print_artistes_choisis()
            time.sleep(1)

        except (ValueError, IndexError):
            print("Veuillez entrer un nombre valide.")
            continue

    return artiste
    
def display_tree(node, level=0):
    '''
    Affiche l'arbre de recommandations de maniere textuelle
    node : noeud courant
    level : niveau du noeud courant
    '''
    if node is not None:
        display_tree(node.droit, level + 1)
        print(' ' * 4 * level + '->', node.valeur['name'])
        display_tree(node.gauche, level + 1)

def get_artist_by_name(name):
    '''
    name : nom de l'artiste recherché
    return : données sur l'artiste correspondant
    '''
    candidats = sp.search(q=name, type='artist', limit=2)
    for artist in candidats['artists']['items']:
        if artist['name'].lower() == name.lower() :
            return artist

def display_tree_graphviz(root):
    '''
    Affiche l'arbre de recommandations avec graphviz
    root : racine de l'arbre
    '''
    print("Affichage de l'arbre de recommandations avec graphviz...")
    dot = graphviz.Digraph()

    def add_edges(node):
        if node.gauche:
            dot.edge(node.valeur['name'], node.gauche.valeur['name'])
            add_edges(node.gauche)
        if node.droit:
            dot.edge(node.valeur['name'], node.droit.valeur['name'])
            add_edges(node.droit)

    add_edges(root)

    dot.render('arbre_recommandations', view=True)


def get_artist_top_tracks(artist_uri):
    '''
    artist_uri : uri de l'artiste
    return : top 10 tracks de l'artiste
    '''
    return sp.artist_top_tracks(artist_uri)

def choose_track(tracks):
    '''
    tracks : catalogue de tracks
    return : track choisie at random (dict)
    '''
    indice = random.randint(0, len(tracks['tracks']) - 1)
    # print(indice)
    return tracks['tracks'][indice]


def print_artistes_choisis() :
    '''
    Affiche les artistes choisis jusqu'à présent
    '''
    print("Artistes choisis jusqu'à présent : " + ", ".join(artistes_choisis))
    time.sleep(1.5)
    

def create_playlist(playlist_name) :
    '''
    Crée une playlist spotify à partir des artistes sélectionnés en parcourant l'arbre de recommandations. 
    Un artiste de l'arbre correspond à une chanson dans la playlist.
    playlist_name : nom de la playlist
    return : url de la playlist créée
    '''

    # on parcourt l'arbre en largeur
    file = File.File()
    file.enfiler(root)
    playlist = File.File()


    while not file.est_vide():
        noeud = file.defiler()
        playlist.enfiler(noeud)

        if noeud.gauche:
            file.enfiler(noeud.gauche)
        if noeud.droit:
            file.enfiler(noeud.droit)

    # on crée une playlist
    playlist_sp = sp.user_playlist_create(sp.me()['id'], playlist_name, public=False, description="Playlist basée sur l'artiste " + root.valeur['name'])

    # on ajoute les chansons à la playlist
    while not playlist.est_vide() :
        artiste = playlist.defiler()
        tracks = get_artist_top_tracks(artiste.valeur['uri'])
        track = choose_track(tracks)
        sp.playlist_add_items(playlist_sp['id'], [track['uri']])
        # print(track['name'])
    
    affichage()
    print("Playlist créée :", playlist_sp['external_urls']['spotify'])
    return playlist_sp['external_urls']['spotify']

def affichage() :
    txt = "Création de la playlist"

    for lettre in txt:
        print(lettre, end="", flush=True)
        time.sleep(0.1)

    for i in range(10):

        print(".", end="", flush=True)
        time.sleep(0.5)
    print()



if __name__ == "__main__" :
    main()

    # bibi = sp.search(q="Bibi", type="artist", limit=5)
    # for artist in bibi['artists']['items']:
    #     print(artist['name'], artist['genres'])

    # print(lastfm.get_similar_artists("offonoff", []))
    # print(drake['artists'] ['items'][0]['name'])
    # top_tracks = get_artist_top_tracks("spotify:artist:0qQI2kmsvSe2ex9k94T5vu")

    # print(choose_track(top_tracks)['name'])