import json
import tweepy
import re
import unidecode

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAMwJiAEAAAAAHRY6uroIJnMMbtXFVde3EDR6fPA' \
               '%3DxW0bEA057h4hVuP66d9U0zlsSomX6EiL8CI51jruE2CcrBVHrd '

fichier = open("dataTwitter.txt", 'a')

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

    i = 0
    for tweet in tweets_list:
        temp = str(tweet.id) + '; ' + str(tweet.created_at) + '; \"' + normaliser_texte(tweet.text) + "\"\n"
        fichier.write(temp)
        i += 1
    print(f"Fin de la récupération de {i} Tweets")


collect_tweet('Redbull -is:retweet lang:en', 3, "data_19-10-2022_2.json")
