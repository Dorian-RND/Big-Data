import tweepy

#Obtenir la clé
CONSUMER_KEY = 'gybAWPZzZqzjCLiefaMNP0F8r'
CONSUMER_SECRET = '4sYS4nPLVbBltqBkGPC2VQLCfZ1tDthrhNGJQ95Olr0pFvwfw6'
#Créer une instance de la classe OAuthHandler
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
ACCESS_TOKEN = '1579367871179808769-6xUWVQenKafV2LasOW4XVKcH343VrG'
ACCESS_SECRET = 'hzVY3qpIgubTuFGP3UnpQRHw7YcoOKYAvrr0lmtqm4nzE'
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

#Authentification OAuth
api = tweepy.API(auth)

tab = []
#Recherchez dans Twitter et écrivez le résultat dans Excel
for status in api.search_tweets(q='"f1"', lang='fr', result_type='popular',count=10):
    print(status._json)
    tab.append(status.text)
