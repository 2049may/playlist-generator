# imports lastfm
import requests
import json
import requests_cache
import cred

requests_cache.install_cache() # pour eviter de refaire des requetes inutiles

def lastfm_get(payload) :
    '''
    payload : dictionnaire contenant les paramètres de la requête
    return : réponse de la requête
    '''
    # headers et url
    headers = {'user-agent': cred.USER_AGENT}
    url = "http://ws.audioscrobbler.com/2.0/"

    # ajouter la clé API et le format
    payload['api_key'] = cred.LASTFM_API_KEY
    payload['format'] = 'json'

    reponse = requests.get(url, headers=headers, params=payload)
    return reponse

def jprint(obj) :
    '''
    affiche un objet json de manière lisible
    obj : objet json
    '''
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def get_similar_artists(artist_name, filter) :
    '''
    artist_name : nom de l'artiste
    filter : liste des noms des artistes déjà choisis
    return : liste des artistes similaires format json
    '''
    r = lastfm_get({'method': 'artist.getsimilar', 'artist': artist_name, 'limit': 30})
    similar_artists = r.json()
    
    # Filter out artists that are in the filter list
    filtered_artists = [artist for artist in similar_artists['similarartists']['artist'] if artist['name'] not in filter]
    
    # Return the filtered list in the same format
    return {'similarartists': {'artist': filtered_artists}}

def print_similar_artists(json, debut=0, fin=10):
    '''
    json : liste des artistes similaires format json
    start : index de début
    end : index de fin
    '''
    artists = json['similarartists']['artist']
    for i in range(debut, min(fin, len(artists))):
        print(f"\t{i + 1} - {artists[i]['name']}")
    


if __name__ == "__main__" :
    r = get_similar_artists("Jiwoo")
    print(r)
    # print(r['similarartists']['artist'][0])
    # print_similar_artists(r)

