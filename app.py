from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import StreamListener
import tweepy

import logging

from translate import Translator

class TranslateStreamListener(StreamListener):

    def __init__(self, auth, src_lang="es", dest_lang="it"):
        super(StreamListener, self).__init__()

        self.api = tweepy.API(auth)
        self.translator = Translator(from_lang=src_lang, to_lang=dest_lang)

    def on_status(self, status):
        tweet_id = status.id_str
        tweet_text = status.text

        reply_text = self.translator.translate(tweet_text)

        logging.debug(
            f"ID: {tweet_id} - TEXT: {tweet_text} - REPLY: {reply_text}"
        )

        self.api.update_status(reply_text, in_reply_to_status_id=tweet_id)

        return True

class App():

    def __init__(self, config):
        self.auth = OAuthHandler(
            config.get("consumer_key"),
            config.get("consumer_secret")
        )

        self.auth.set_access_token(
            config.get("access_token"),
            config.get("access_token_secret")
        )

        self.user_id = config.get("user_id")

        self.stream = Stream(self.auth, TranslateStreamListener(self.auth))

    def run(self):
        self.stream.filter(follow=[self.user_id])
