import threading
from loader import logger
from vk.update_widget import update_every_seconds
from web_app.callback import app


logger.info("Start thread for update widget")
widget = threading.Thread(target=update_every_seconds, args=(300,), daemon=True)
widget.start()
logger.info("Start flask app")