import tweepy


if __name__ == '__main__':

    auth = tweepy.OAuth1UserHandler(
        "gybAWPZzZqzjCLiefaMNP0F8r", "4sYS4nPLVbBltqBkGPC2VQLCfZ1tDthrhNGJQ95Olr0pFvwfw6", "1579367871179808769-6xUWVQenKafV2LasOW4XVKcH343VrG", "hzVY3qpIgubTuFGP3UnpQRHw7YcoOKYAvrr0lmtqm4nzE"
    )

    api = tweepy.API(auth)

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)
