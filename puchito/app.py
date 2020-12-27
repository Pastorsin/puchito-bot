from tweepy import OAuthHandler
from tweepy import Stream

import logging

from .config import Config
from .listener import TranslateReplyStreamListener


class App():

    def __init__(self, config: Config):
        logging.debug("Starting app")

        self.auth = OAuthHandler(
            config.consumer_key,
            config.consumer_secret
        )

        self.auth.set_access_token(
            config.access_token,
            config.access_token_secret
        )

        self.user_id = config.user_id

        listener = TranslateReplyStreamListener(self.auth, self.user_id)
        self.stream = Stream(self.auth, listener)

    def run(self):
        self.stream.filter(follow=[self.user_id])
