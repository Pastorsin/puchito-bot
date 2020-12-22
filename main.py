import os
import logging

import App

CONFIG = {
    "consumer_key": os.environ.get('consumer_key', None),
    "consumer_secret": os.environ.get('consumer_secret', None),
    "access_token": os.environ.get('access_token', None),
    "access_token_secret": os.environ.get('access_token_secret', None),
    "user_id": os.environ.get('user_id', None)
}

LOG_FILENAME = "app.log"


def main():
    logging.basicConfig(
        filename=LOG_FILENAME,
        filemode='w',
        format='%(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )

    logging.debug("Starting app")

    app = App(CONFIG)
    app.run()


if __name__ == '__main__':
    main()
