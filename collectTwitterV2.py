import json
import tweepy
import re
import unidecode

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAMwJiAEAAAAAHRY6uroIJnMMbtXFVde3EDR6fPA' \
               '%3DxW0bEA057h4hVuP66d9U0zlsSomX6EiL8CI51jruE2CcrBVHrd '

# Fonction qui permet de normaliser un texte en paramètre
#   - Supprime les url
#   - Supprime les retours à la ligne
#   - Change les " en '
#   - Normalise les caractères spéciaux (é en e)
#   - Les # en rien
#   - Les @ en rien
def normaliser_texte(texte):
    temp_text = texte
    temp_text = re.sub(r'http\S+', '', temp_text)
    temp_text = re.sub('\n', "", temp_text)
    temp_text = re.sub('\"', "'", temp_text)
    temp_text = unidecode.unidecode(temp_text)
    temp_text = re.sub('#', "", temp_text)
    temp_text = re.sub('@', "", temp_text)
    return temp_text


# Cette fonction permet de récuperer des tweets à partir de filtres et des stockés dans un fichier JSON
# Paramètres :
#   - Liste de filtres
#   - Langue des tweets
#   - Nombre de tweets que l'on veut récuperer
#   - Nom du fichier JSON ou stocker les données.
def collect_tweet(filtres, nb_tweet, fichier_json):

    # Put your Bearer Token in the parenthesis below
    client = tweepy.Client(bearer_token=BEARER_TOKEN)

    print(f"Début de la récupérations des tweets avec comme filtre : {filtres}...")
    tweets_list = tweepy.Paginator(client.search_recent_tweets,
                                   query=filtres,
                                   max_results=10,
                                   tweet_fields=['created_at', 'text', 'id']).flatten(limit=nb_tweet)

    data = []
    i = 0
    for tweet in tweets_list:
        temp = {"id": tweet.id,
                "created_at": str(tweet.created_at),
                "text": normaliser_texte(tweet.text),
                }
        data.append(temp)
        i += 1
    print(f"Fin de la récupération de {i} Tweets")

    # Ajouter le dico dans un fichier JSON
    with open(fichier_json, "w") as outfile:
        json.dump(data, outfile, indent=4)

    print(f"Les données sont au format JSON dans le fichier : {fichier_json} ")


collect_tweet('Redbull -is:retweet lang:en', 1000, "data_19-10-2022.json")
