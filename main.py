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

# erreur de path, donc ajout du path de graphviz manuellement
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

requests_cache.install_cache() # pour éviter de refaire les requêtes

# imports spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# authentification
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.SPOTIFY_CLIENT_ID,
                                               client_secret=cred.SPOTIFY_CLIENT_SECRET,
                                               redirect_uri="http://127.0.0.1:9090",
                                               scope="user-library-read playlist-modify-public playlist-modify-private"))

#TODO : gestion d'erreurs, ne pas mettre le meme artiste 2 fois
#TODO : si un artiste n'a pas de similar artists, soit : 
#                   * la branche s'arrete et on parcourt les autres noeuds jusqu'à ce qu'on ait 15 artistes (plutot ça je pense)
#                   * soit on regénère un noeud

def main() :
    global root
    global nom_playlist
    '''
    Fonction principale
    '''
    
    # query = input("Sur quel artiste voulez-vous baser votre playlist ? ")
    query = "Tabber"
    result_type = "artist" # type de résultat recherché
    nb_max = 12 # nombre maximum d'artistes dans l'arbre = nombre de chansons dans la playlist

    results = sp.search(q=query, type=result_type, limit=5) 


    nom_playlist = query + "vibes"
    description_playlist = "Playlist basée sur l'artiste " + query


    # affichage des résultats
    print(f"Résultats pour {query} :")
    k = 1
    for artist in results['artists']['items']:
        if artist['genres']:
            genres = f"Genres: {', '.join(artist['genres'])}"
        else:
            genres = "Genres: Unknown"
        # print(f"{k} - {artist['name']}, {genres}, URI: {artist['uri']}")
        print(f"\t{k} - {artist['name']}, {genres}")
        k += 1
        print()

    choix = -1
    while choix < 0 or choix >= len(results['artists']['items']):    
        try :
            # choix = int(input("Choisissez l'artiste que vous recherchez (saisir son numéro) : "))-1
            choix = 0
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
    construire_arbre(root, 1, nb_max)
    
    # affichage de l'arbre avec graphviz
    display_tree_graphviz(root)

    nom_playlist = input("Entrez le nom de la playlist : ")

    print(create_playlist(nom_playlist))


def construire_arbre(noeud, nb_noeuds, nb_max) :
    '''
    noeud : noeud racine de l'arbre au premier appel, puis noeud courant à chaque appel récursif
    nb_noeuds : nombre de noeuds courants
    nb_max : nombre de noeuds maximum (15 par défaut)
c    construit l'arbre de recommandations à partir de l'artiste racine, arbre construit de manière récursive en largeur
    '''
    global artistes_choisis

    print("nb noeuds : ", nb_noeuds)
    file = File.File()
    file.enfiler((noeud, 1))
    artistes_choisis = [root.valeur['name']]
    niveau = 0

    while not file.est_vide() and nb_noeuds < nb_max:
        noeud, niveau = file.defiler()

        if niveau >= 4 :
            continue

        json_artistes = lastfm.get_similar_artists(noeud.valeur['name'], artistes_choisis)
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

            try:
                fg, fd = choix.split(" ")
                if len(fg) == 0 or len(fd) == 0:
                    raise ValueError("Invalid number of arguments")
                fg, fd = int(fg) - 1, int(fd) - 1

                if fg < 0 or fd < 0 or fg >= len(json_artistes['similarartists']['artist']) or fd >= len(json_artistes['similarartists']['artist']):
                    raise ValueError("Invalid artist number")
            
            except ValueError:
                print("==============================================================================")
                print("Entrée invalide. Veuillez entrer deux numéros valides séparés par un espace.")
                print()
                continue
            except Exception:
                print("==============================================================================")
                print("Entrée invalide. Veuillez entrer exactement deux numéros séparés par un espace.")
                continue

            nom_gauche = json_artistes['similarartists']['artist'][fg]['name']
            nom_droit = json_artistes['similarartists']['artist'][fd]['name']

            print("Vous avez choisi : " + nom_gauche + " et " + nom_droit)
            print()

            time.sleep(0.5)

            artistes_choisis.append(nom_gauche)
            artistes_choisis.append(nom_droit)
            
            print_artistes_choisis()

            print("nb noeuds : ",nb_noeuds)

            artiste_gauche = get_artist_by_name(nom_gauche)
            artiste_droit = get_artist_by_name(nom_droit)

            if artiste_gauche is None :
                artistes_choisis.remove(nom_gauche)
                print("Impossible de trouver l'artiste " + nom_gauche)
                lastfm.print_similar_artists(json_artistes, debut, debut + 10)

                while artiste_gauche is None:
                    try:
                        choix = input("Veuillez choisir un autre artiste : ")
                        print()

                        if len(choix.split()) != 1:
                            raise ValueError("Invalid number of arguments")
                        
                        choix = int(choix)
                        nom_gauche = json_artistes['similarartists']['artist'][int(choix) - 1]['name']
                        artiste_gauche = get_artist_by_name(nom_gauche)

                        print("Vous avez choisi : " + nom_gauche)

                        artistes_choisis.append(nom_gauche)

                        print_artistes_choisis()
                        time.sleep(0.5)

                    except (ValueError, IndexError):
                        print("Veuillez entrer un nombre valide.")
                        continue


            if artiste_droit is None :
                artistes_choisis.remove(nom_droit)
                print("Impossible de trouver l'artiste " + nom_droit)
                lastfm.print_similar_artists(json_artistes, debut, debut + 10)

                while artiste_droit is None:
                    try:
                        choix = input("Veuillez choisir un autre artiste : ")
                        print()

                        if len(choix.split()) != 1:
                            raise ValueError("Invalid number of arguments")
                        
                        choix = int(choix)
                        nom_droit = json_artistes['similarartists']['artist'][int(choix) - 1]['name']
                        artiste_droit = get_artist_by_name(nom_droit)

                        print("Vous avez choisi : " + nom_droit)

                        artistes_choisis.append(nom_droit)

                        print_artistes_choisis()
                        time.sleep(0.5)

                    except (ValueError, IndexError):
                        print("Veuillez entrer un nombre valide.")
                        continue


            fg_node = Noeud({'name': artiste_gauche['name'], 'uri': artiste_gauche['uri']})
            fd_node = Noeud({'name': artiste_droit['name'], 'uri': artiste_droit['uri']})

            noeud.gauche = fg_node
            noeud.droit = fd_node

            nb_noeuds += 2
            choisi = True

            continuer = int(input("Continuer ? (1 pour continuer, 0 pour supprimer un artiste) : "))
            print()
            # os.system('cls')

            # TODO : supprimer un artiste

            # if continuer == 0:
            #     for artist in artistes_choisis:
            #         if artist != root.valeur['name']:
            #             print("\t", artistes_choisis.index(artist) + 1, "-", artist)
            #     suppr = int(input("Quel artiste voulez-vous supprimer ? (saisir son numéro) : "))
            #     artiste_a_supprimer = artistes_choisis[suppr - 1]

            #     if artiste_a_supprimer == root.valeur['name']:
            #         print("Impossible de supprimer l'artiste de base.")
            #     else:
            #         noeud_a_supprimer = root.recherche(artiste_a_supprimer, dict=True)
            #         if noeud_a_supprimer:
            #             root.supprimer(artiste_a_supprimer)
            #             artistes_choisis.pop(suppr - 1)
            #         else:
            #             print(f"Artiste {artiste_a_supprimer} non trouvé dans l'arbre.")

            #     print("Vous avez supprimé : " + artiste_a_supprimer)
            #     print(artistes_choisis)

            #     print()
            #     time.sleep(1)
            #     lastfm.print_similar_artists(json_artistes, debut, debut + 10)
            #     print()
            #     nouveau_choix = int(input("Veuillez selectionner un nouvel artiste (taper son numéro) : "))
            #     print()

            #     nouvel_artiste = json_artistes['similarartists']['artist'][nouveau_choix - 1]['name']
            #     print("Vous avez choisi : " + nouvel_artiste)
            #     artistes_choisis.append(nouvel_artiste)
            #     print_artistes_choisis()


            print()

            file.enfiler((fg_node, niveau + 1))
            file.enfiler((fd_node, niveau + 1))

            print("=============================================================")

    return nb_noeuds
    
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
    

def create_playlist(playlist_name) :
    '''
    Crée une playlist spotify à partir des artistes sélectionnés en parcourant l'arbre de recommandations. 
    Un artiste de l'arbre correspond à une chanson dans la playlist.
    '''


    # on parcourt l'arbre en largeur
    file = File.File()
    file.enfiler(root)
    artistes = []

    while not file.est_vide():
        noeud = file.defiler()
        artistes.append(noeud)

        if noeud.gauche:
            file.enfiler(noeud.gauche)
        if noeud.droit:
            file.enfiler(noeud.droit)

    # on crée une playlist
    # playlist = sp.user_playlist_create(sp.me()['id'], playlist_name, public=False, description="Playlist basée sur l'artiste " + root.valeur['name'])

    # on ajoute les chansons à la playlist
    for artiste in artistes:
        tracks = get_artist_top_tracks(artiste.valeur['uri'])
        track = choose_track(tracks)
        # sp.playlist_add_items(playlist['id'], [track['uri']])
        print(track['name'])
    
    # return playlist['external_urls']['spotify']


if __name__ == "__main__" :
    # main()
    # bibi = sp.search(q="Bibi", type="artist", limit=5)
    # for artist in bibi['artists']['items']:
    #     print(artist['name'], artist['genres'])

    print(get_artist_by_name("Bibi"))
    # print(drake['artists'] ['items'][0]['name'])
    # top_tracks = get_artist_top_tracks("spotify:artist:0qQI2kmsvSe2ex9k94T5vu")
    
    # print every key in the catalog
    # for key in top_tracks['tracks'][0].keys():
        # print(key)

    # print the name of the first track
    # print(top_tracks['tracks'][0]['name'])

    # print the url of the first track
    # print(top_tracks['tracks'][0]['external_urls']['spotify'])

    # print(choose_track(top_tracks)['name'])