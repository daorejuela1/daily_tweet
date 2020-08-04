import requests
from random import randrange
import tweepy
import os
import time
from os import environ

consumer_key = environ['API_KEY']
consumer_secret_key = environ['API_SECRET_KEY']
access_token = environ['ACCESS_TOKEN']
access_token_secret = environ['ACCESS_TOKEN_SECRET']
# INTERVAL = 60 * 60 * 24  # tweet every 24 hours
INTERVAL = 60  # every 60 seconds, for testing

def get_random_quote():
    """
    Gets a random quote from the They Said So API
    :return: quote or ask again in any error case
    """
    today_theme = randrange(0, 6)
    tag_wheel = ['inspire', 'management', 'life', 'funny','love','art','students']
    url = 'https://quotes.rest/qod?category=' + tag_wheel[today_theme]
    response = requests.get(url)
    if response.status_code == 200:
        quotes = response.json()['contents']['quotes'][0]
        if int(quotes['length']) >= 250:
            tweet_quote()
        else:
            return quotes
    else:
        tweet_quote()


def create_tweet():
    """
    Creates the message to publish the tweet
    :return: String with the tweet
    """
    quotes = get_random_quote()
    if not quotes:
        tweet_quote()
    download_image(quotes['background'])
    message = quotes['title'] + "\n\n" + "\"" + quotes['quote'] + "\"" + " -- " + quotes['author']
    for tags in quotes['tags']:
        message = message + " #" + tags
    message += " #TheySaidSo"
    return message


def download_image(url):
    """
    Downloads image to upload it to twitter
    :param url: url of the image to download
    :return: Nothing
    """
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
    else:
        tweet_quote()


def tweet_quote():
    """
    Logs in to tweet API
    :return: Nothing
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    tweet_message = create_tweet()
    api.update_with_media("temp.jpg", tweet_message)
    os.remove("temp.jpg")
    print("Tweet displayed")


if __name__ == "__main__":
    while True:
        tweet_quote()
        time.sleep(INTERVAL)
