import logging
import sys
import os

from .app import App
from .config import Config

def main():

    logging.basicConfig(
        format='%(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(filename="app.log", mode="w"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    config = Config(
        consumer_key=os.environ.get('consumer_key', None),
        consumer_secret=os.environ.get('consumer_secret', None),
        access_token=os.environ.get('access_token', None),
        access_token_secret=os.environ.get('access_token_secret', None),
        user_id=os.environ.get('user_id', None),
    )

    app = App(config)
    app.run()


if __name__ == '__main__':
    main()
