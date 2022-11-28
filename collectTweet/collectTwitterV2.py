import json
import time

import tweepy
import re
import unidecode
import geonamescache
import tqdm
from datetime import date

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAMwJiAEAAAAAHRY6uroIJnMMbtXFVde3EDR6fPA%3DxW0bEA057h4hVuP66d9U0zlsSomX6EiL8CI51jruE2CcrBVHrd '

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
    temp_text = re.sub(',', "", temp_text)
    temp_text = re.sub(';', "", temp_text)
    temp_text = re.sub("\*", "", temp_text)
    temp_text = re.sub('\|', "", temp_text)
    temp_text = re.sub('&gt;', "", temp_text)
    temp_text = re.sub('&lt;', "", temp_text)
    temp_text = re.sub('&amp;', "", temp_text)
    temp_text = unidecode.unidecode(temp_text)

    separateur = " "
    cleanText = []

    textSplit = temp_text.split(separateur)
    for word in textSplit:
        if not word.startswith("@"):
            cleanText.append(word)

    return str(separateur.join(cleanText))


def getClearLocation(paysUser, tabPays):
    for pays in tabPays:
        if pays in paysUser:
            return str(pays)
    return "NULL"


# Cette fonction permet de récuperer des tweets à partir de filtres et des stockés dans un fichier JSON
# Paramètres :
#   - Liste de filtres
#   - Langue des tweets
#   - Nombre de tweets que l'on veut récuperer
#   - Nom du fichier JSON ou stocker les données.
def collect_tweet(filtres, nb_tweet):

    # Put your Bearer Token in the parenthesis below
    client = tweepy.Client(bearer_token=BEARER_TOKEN,
                           wait_on_rate_limit=True)

    print(f"Début de la récupérations des tweets avec comme filtre : {filtres}...")
    tweets_list = tweepy.Paginator(client.search_recent_tweets,
                                   query=filtres,
                                   max_results=100,
                                   tweet_fields=['created_at', 'text', 'id', 'public_metrics', "author_id"]).flatten(limit=nb_tweet)
    print("Fin recuperation tweet")
    return tweets_list


def putTweetCSV(listTweet, fichierTweet):
    fichier = open(fichierTweet, "a", encoding="utf-8")

    CONSUMER_KEY = 'zp07WHXd59oWkw6wOjEV2YPYI'
    CONSUMER_SECRET = 'xygZUyJ8qmz1Mf0dBw7TCqvo4Px6CmsiMlbTLqPd4GJFpDw1fD'
    ACCESS_TOKEN = '1579367871179808769-WKWgKpSTHofVYcw0JaTjnDDAjuaBKM'
    ACCESS_SECRET = 'HGqNNK6trXm3Ry1DQcPL4IdhRe9DfhOG6WzWyC5TW2OL8'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Initialisation du tableau contenant les pays
    gc = geonamescache.GeonamesCache()
    dictPays = gc.get_countries()
    dictPaysUS = gc.get_us_states()
    listPays = []
    for key in dictPays:
        listPays.append(dictPays[key]['name'])
    for key in dictPaysUS:
        listPays.append(dictPaysUS[key]['name'])

    print("Écriture dans CSV ...")
    fichier.write("tweet_id,tweet_date,tweet_text,tweet_localisation,nb_RT,nb_Like\n")
    i = 0
    for tweet in tqdm.tqdm(listTweet):

        # fetching the user
        user = api.get_user(user_id=tweet.author_id)
        # fetching the location
        location = normaliser_texte(user.location)

        # temp = str(tweet.id) + ', ' + str(tweet.created_at) + ', ' + normaliser_texte(tweet.text) + "\n"
        temp = str(tweet.id) + ',' + str(tweet.created_at) + "," + str(getClearLocation(location, listPays)) + ',' + normaliser_texte(tweet.text) + ',' + str(tweet.public_metrics["retweet_count"]) + ',' + str(tweet.public_metrics["like_count"]) + "\n"
        fichier.write(temp)
        # fichier.write(temp)
        i += 1


nom_fichier = "data_" + str(date.today()).replace("-", "_") + "_AVEC_PAYS.txt"
tweetList = collect_tweet('Redbull -is:retweet lang:en', 30000)
putTweetCSV(tweetList, nom_fichier)

