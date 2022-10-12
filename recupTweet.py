import tweepy

# Fill the X's with the credentials obtained by
# following the above-mentioned procedure.
consumer_key = "gybAWPZzZqzjCLiefaMNP0F8r"
consumer_secret = "4sYS4nPLVbBltqBkGPC2VQLCfZ1tDthrhNGJQ95Olr0pFvwfw6"
access_key = "1579367871179808769-6xUWVQenKafV2LasOW4XVKcH343VrG"
access_secret = "hzVY3qpIgubTuFGP3UnpQRHw7YcoOKYAvrr0lmtqm4nzE"

# Function to extract tweets
def get_tweets(username):
    # Authorization to consumer key and consumer secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # Access to user's access key and access secret
    auth.set_access_token(access_key, access_secret)

    # Calling api
    api = tweepy.API(auth)

    # 200 tweets to be extracted
    number_of_tweets = 5
    tweets = api.user_timeline(screen_name=username)
   # print(tweets)
    # Empty Array
    tmp = []

    # create array of tweet information: username,
    # tweet id, date/time, text
    tweets_for_csv = [tweet.text for tweet in tweets]  # CSV file created
    for j in tweets_for_csv:
        # Appending tweets to the empty array tmp
        tmp.append(j)

        # Printing the tweets
    print(len(tmp))
    print(tmp)


# Driver code
if __name__ == '__main__':
    # Here goes the twitter handle for the user
    # whose tweets are to be extracted.
    get_tweets("Kammeto")