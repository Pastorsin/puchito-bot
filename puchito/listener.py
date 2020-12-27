import logging

from tweepy import StreamListener
from tweepy import API

from translate import Translator


class TranslateReplyStreamListener(StreamListener):

    def __init__(self, auth, user_to_reply, src_lang="es", dest_lang="it"):
        super(StreamListener, self).__init__()

        self.api = API(auth)
        self.user_to_reply = user_to_reply

        self.translator = Translator(from_lang=src_lang, to_lang=dest_lang)

    def on_status(self, status) -> bool:
        tweet_id = status.id_str
        tweet_text = status.text
        tweet_user_id = status.user.id_str

        logging.debug(f"ID: {tweet_id}")
        logging.debug(f"TEXT: {tweet_text} - USER: {tweet_user_id}")

        if (self.is_user_to_reply(tweet_user_id)):
            reply = self.reply(tweet_text)

            self.api.update_status(
                reply,
                tweet_id,
                auto_populate_reply_metadata=True
            )

            logging.debug(f"REPLY: {reply}")

        return True

    def reply(self, tweet_text: str) -> str:
        return self.translator.translate(tweet_text)

    def is_user_to_reply(self, tweet_user_id: str) -> bool:
        return self.user_to_reply == tweet_user_id
