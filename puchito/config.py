import logging

from dataclasses import dataclass


class EmptyAtributtesException(Exception):
    pass


@dataclass
class Config:
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str
    user_id: str

    def __post_init__(self):
        if self.__empty_attributes():
            logging.error("Invalid configuration, missing attributes.")
            raise EmptyAtributtesException()

        logging.debug("Configuration established successfully.")

    def __empty_attributes(self):
        return not all(vars(self).values())
