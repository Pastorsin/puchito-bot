from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import StreamListener
import tweepy

import logging

from translate import Translator

class TranslateReplyStreamListener(StreamListener):

    def __init__(self, auth, user_to_reply, src_lang="es", dest_lang="it"):
        super(StreamListener, self).__init__()

        self.api = tweepy.API(auth)
        self.user_to_reply = user_to_reply

        self.translator = Translator(from_lang=src_lang, to_lang=dest_lang)

    def on_status(self, status):
        tweet_id = status.id_str
        tweet_text = status.text
        tweet_user_id = status.user.id_str

        logging.debug(
            f"ID: {tweet_id} - TEXT: {tweet_text} - USER: {tweet_user_id}"
        )

        if (self.user_to_reply == tweet_user_id):
            reply_text = self.translator.translate(tweet_text)

            self.api.update_status(
                reply_text,
                tweet_id,
                auto_populate_reply_metadata=True
            )

            logging.debug(f"REPLY: {reply_text}")

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

        listener = TranslateReplyStreamListener(self.auth, self.user_id)
        self.stream = Stream(self.auth, listener)

    def run(self):
        self.stream.filter(follow=[self.user_id])
