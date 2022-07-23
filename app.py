import threading

from loader import logger
from vk.update_widget import update_every_seconds
from web_app.callback import app

def main():
    logger.info("Start thread for update widget")
    widget = threading.Thread(target=update_every_seconds, args=(300,), daemon=True)
    widget.start()
    logger.info("Start flask app")
    app.run()


if __name__ == "__main__":
    main()