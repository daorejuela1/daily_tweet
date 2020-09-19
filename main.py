from random import randrange
from os import environ
import credentials
import requests
import schedule
import tweepy
import random
import os
import time

# consumer_key = credentials.API_KEY
# consumer_secret_key = credentials.API_SECRET_KEY
# access_token = credentials.ACCESS_TOKEN
# access_token_secret = credentials.ACCESS_TOKEN_SECRET
consumer_key = environ['API_KEY']
consumer_secret_key = environ['API_SECRET_KEY']
access_token = environ['ACCESS_TOKEN']
access_token_secret = environ['ACCESS_TOKEN_SECRET']
image_name = "temp.jpg"
global tweet_counter
tweet_counter = 0


def get_random_quote():
    """
    Gets a random quote from the They Said So API
    :return: quote or ask again in any error case
    """
    global tweet_counter
    tag_wheel = ['inspire', 'management', 'life',
                 'love', 'art', 'students', 'funny']
    if tweet_counter == 0:
        week_order = random.sample(range(len(tag_wheel)), len(tag_wheel))
    today_theme = week_order[tweet_counter]
    url = "https://quotes.rest/qod?category={}".format(tag_wheel[today_theme])
    response = requests.get(url)
    if response.status_code == 200:
        quotes = response.json()['contents']['quotes'][0]
        if int(quotes['length']) <= 200:
            tweet_counter += 1
            if (tweet_counter == 7):
                tweet_counter = 0
            return quotes
    return None


def create_tweet():
    """
    Creates the message to publish the tweet
    :return: String with the tweet
    """
    quotes = get_random_quote()
    while quotes is None:
        quotes = get_random_quote()
    download_image(quotes['background'])
    message = """{}

"{}" -- {}""".format(quotes['title'], quotes['quote'], quotes['author'])
    for tags in quotes['tags']:
        tags = tags.title()
        tags = tags.replace("-", "")
        message = message + " #" + tags
    message += " #TheySaidSo"
    return message


def download_image(url):
    """
    Downloads image to upload it to twitter
    :param url: url of the image to download
    :return: Nothing
    """
    filename = image_name
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)


def tweet_quote():
    """
    Logs in to tweet API
    :return: Nothing
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    tweet_message = create_tweet()
    api.update_with_media(image_name, tweet_message)
    os.remove(image_name)
    print("Tweet displayed")

schedule.every().day.at("15:15").do(tweet_quote)

if __name__ == "__main__":
    """
    Runs scheduled tweet
    """
     while True:
        schedule.run_pending()
        time.sleep(1)