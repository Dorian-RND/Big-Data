import json
from datetime import date
import geonamescache
import tqdm
import tweepy
import re
import unidecode


def normaliser_texte(texte):
    temp_text = texte
    temp_text = re.sub(r'http\S+', '', temp_text)
    temp_text = re.sub('\n', "", temp_text)
    temp_text = re.sub('\"', "'", temp_text)
    temp_text = re.sub(',', "", temp_text)
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
        if pays in paysUser :
            return str(pays)
    return ""


def collect_tweet(filtres, nb_tweet):
    CONSUMER_KEY = 'zp07WHXd59oWkw6wOjEV2YPYI'
    CONSUMER_SECRET = 'xygZUyJ8qmz1Mf0dBw7TCqvo4Px6CmsiMlbTLqPd4GJFpDw1fD'
    ACCESS_TOKEN = '1579367871179808769-WKWgKpSTHofVYcw0JaTjnDDAjuaBKM'
    ACCESS_SECRET = 'HGqNNK6trXm3Ry1DQcPL4IdhRe9DfhOG6WzWyC5TW2OL8'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Recuperation des tweets
    print(f"Début de la récupérations des tweets avec comme filtre : {filtres}...")
    tweets_list = tweepy.Cursor(api.search_tweets, q=filtres, tweet_mode="extended").items(nb_tweet)
    print("Fin recuperation tweet")
    return tweets_list


def putTweetCSV(listTweet, fichierTweet):

    fichier = open(fichierTweet, "a", encoding="utf-8")

    CONSUMER_KEY = 'zp07WHXd59oWkw6wOjEV2YPYI'
    CONSUMER_SECRET = 'xygZUyJ8qmz1Mf0dBw7TCqvo4Px6CmsiMlbTLqPd4GJFpDw1fD'
    ACCESS_TOKEN = '1579367871179808769-WKWgKpSTHofVYcw0JaTjnDDAjuaBKM'
    ACCESS_SECRET = 'HGqNNK6trXm3Ry1DQcPL4IdhRe9DfhOG6WzWyC5TW2OL8'
    # auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    # auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    # api = tweepy.API(auth, wait_on_rate_limit=True)

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
    i = 0
    for tweet in tqdm.tqdm(listTweet):
        # fetching the user
        # user = api.get_user(user_id=tweet.author_id)
        # fetching the location
        # location = normaliser_texte(user.location)

        temp = str(tweet._json["id"]) + ', ' + str(tweet._json["created_at"]) + ', ' + normaliser_texte(tweet._json["full_text"]) + "\n"
        # temp = str(tweet.id) + ', ' + str(tweet.created_at) + ", " + str(getClearLocation(location, listPays)) + ', ' + normaliser_texte(tweet.text) + "\n"
        fichier.write(temp)
        # fichier.write(temp)
        i += 1

    print(f"Les données sont au format JSON dans le fichier : {fichierTweet} ")


nom_fichier = "data_" + str(date.today()).replace("-", "_") + "_SANS_PAYS.txt"
tweetList = collect_tweet(['Redbull', '-is:retweet', 'lang:en'], 100)
putTweetCSV(tweetList, nom_fichier)

