import time

from database import Session
from database.schemas.user import User
from loader import config, logger
from utils.vk_exceptions import VkApiError
from vk.api import method
from vk.execute import ExecuteCode


def update_every_seconds(seconds=10):
    while True:
        logger.info("Updating widget")
        session = Session()
        try:
            params = {"all_users": User.get_all(session),
                      "top_users": User.get_top_10(session),
                      "title": config.table.title}
            code = ExecuteCode.update_widget.value % params
            logger.debug(code)
            logger.info(len(code))
            a = method("appWidgets.update",
                       access_token=config.group.widget_token,
                       type="table",
                       code=code)
            logger.debug(a)
        except VkApiError as e:
            logger.critical(e)
        logger.info(f"Wait {seconds} seconds")
        session.close()
        time.sleep(seconds)