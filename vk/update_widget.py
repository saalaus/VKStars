from database import Session
from database.schemas.user import User
import time

from loader import config, logger
from utils.vk_exceptions import VkApiError
from vk.execute import ExecuteCode

from vk.api import method


def update_every_seconds(seconds):
    while True:
        logger.info("Updating widget")
        session = Session()
        try:
            params = {"all_users": User.get_all(session), "top_10": User.get_top_10(session),
                      "title": config.table.title}
            a = method("appWidgets.update",
                       access_token=config.group.widget_token,
                       type="table",
                       code=ExecuteCode.update_widget.value % params)
        except VkApiError as e:
            logger.critical(e)
        logger.info(f"Wait {seconds} seconds")
        session.close()
        time.sleep(seconds)
