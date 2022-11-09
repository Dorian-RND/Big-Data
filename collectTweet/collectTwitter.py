import json
import tweepy
import re
import unidecode


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
def collect_tweet(filtres, langue, nb_tweet, fichier_json):
    # Obtenir la clé
    CONSUMER_KEY = 'gybAWPZzZqzjCLiefaMNP0F8r'
    CONSUMER_SECRET = '4sYS4nPLVbBltqBkGPC2VQLCfZ1tDthrhNGJQ95Olr0pFvwfw6'

    # Créer une instance de la classe OAuthHandler
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    ACCESS_TOKEN = '1579367871179808769-6xUWVQenKafV2LasOW4XVKcH343VrG'
    ACCESS_SECRET = 'hzVY3qpIgubTuFGP3UnpQRHw7YcoOKYAvrr0lmtqm4nzE'
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Authentification OAuth
    api = tweepy.API(auth)

    # Recuperation des tweets
    print(f"Début de la récupérations des tweets avec comme filtre : {filtres}...")
    tweets_list = tweepy.Cursor(api.search_tweets, q=filtres, lang=langue, tweet_mode="extended").items(nb_tweet)

    # Initialisations
    dico = dict()
    i = 0
    for tweet in tweets_list:
        temp = {"id": tweet._json["id"],
                "created_at": tweet._json["created_at"],
                "text": tweet._json["full_text"],
                "hashtags": tweet._json["entities"]["hashtags"]
                }
        dico[i + 1] = temp
        i += 1
    print(f"Fin de la récupération de {i} Tweets")

    # Ajouter le dico dans un fichier JSON
    with open(fichier_json, "w") as outfile:
        json.dump(dico, outfile, indent=4)

    print(f"Les données sont au format JSON dans le fichier : {fichier_json} ")


collect_tweet(['Redbull'], "en", 2000, "data.json")
