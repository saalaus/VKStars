import threading
import logging
logger = logging.getLogger('VKStars')
logging.basicConfig(level=logging.DEBUG)

from widget_update import update_widget

logger.info("Start thread for update widget")
widget = threading.Thread(target=update_widget, daemon=True)
widget.start()
logger.info("Start flask app")


