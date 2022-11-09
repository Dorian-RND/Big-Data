# Importing Tweepy and time
import time

import tweepy
import re
import unidecode

fichier = open("dataTwitter.txt", 'a')


# Fonction qui permet de normaliser un texte en paramètre
def normaliser_texte(texte):
    temp_text = re.sub(r'http\S+', '', texte)
    temp_text = re.sub('\n', "", temp_text)
    temp_text = re.sub('\"', "'", temp_text)
    temp_text = unidecode.unidecode(temp_text)
    temp_text = re.sub('#', "", temp_text)
    # temp_text = re.sub('@', "", temp_text)
    temp_text = re.sub(';', "", temp_text)
    return temp_text


# Credentials (INSERT YOUR KEYS AND TOKENS IN THE STRINGS BELOW)
API_KEY = 'vWMAXXGiyqXrtFKTSy0o4csCV'
API_SECRET = 'bokTTEjRIdtNacoOL6clUrkPrMn6qA0cHpn3Qx96qMR99qlksC'
ACCESS_TOKEN = '1579367871179808769-6xUWVQenKafV2LasOW4XVKcH343VrG'
ACCESS_SECRET = 'hzVY3qpIgubTuFGP3UnpQRHw7YcoOKYAvrr0lmtqm4nzE'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAMwJiAEAAAAAHRY6uroIJnMMbtXFVde3EDR6fPA' \
               '%3DxW0bEA057h4hVuP66d9U0zlsSomX6EiL8CI51jruE2CcrBVHrd '

# Gainaing access and connecting to Twitter API using Credentials
client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

data = []

MAX_TWEET = 200


# Bot searches for tweets containing certain keywords
class MyStream(tweepy.StreamingClient):
    nbTweet = 0

    # This function gets called when the stream is working
    def on_connect(self):
        print("Connected\n")

    # This function gets called when a tweet passes the stream
    def on_tweet(self, tweet):
        temp = str(tweet.id) + '; ' + str(tweet.created_at) + '; \"' + normaliser_texte(tweet.text) + "\"\n"
        fichier.write(temp)
        self.nbTweet += 1
        print("-----------------------------------------------")
        print(normaliser_texte(tweet.text))
        print(f"Progression : {(self.nbTweet * 100) / MAX_TWEET} %")
        if self.nbTweet == MAX_TWEET:
            time.sleep(1)
            self.disconnect()


# Creating Stream object
stream = MyStream(bearer_token=BEARER_TOKEN)

# Adding terms to search rules
# It's important to know that these rules don't get deleted when you stop the
# program, so you'd need to use stream.get_rules() and stream.delete_rules()
# to change them, or you can use the optional parameter to stream.add_rules()
# called dry_run (set it to True, and the rules will get deleted after the bot
# stopped running).
stream.add_rules(tweepy.StreamRule("Redbull lang:en -is:retweet"))
stream.get_rules()

print(f"Les règles de filtrages du stream : {str(stream.get_rules())}\n")
stream.filter(tweet_fields=["text", "created_at"])
