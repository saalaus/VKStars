import requests
import re
import time

from exceptions import VkApiError
from const import TOKEN, API_VERSION
import logging
logger = logging.getLogger('VKStars')
logging.basicConfig(level=logging.DEBUG)



last_request = [0.0]


URL = 'https://api.vk.com/method/'
HEADER = {
    'user-agent': "VKAndroidApp/5.23-2978 (Android 4.4.2; SDK 19; x86; unknown Android SDK built for x86; en; 320x240)"}


def method(method: str, **params):
    """main function to call VK methods

    @param method: str: method name
    @param **params: method option

    """
    # logger.debug(f"Method {method} with params {params}")
    if "access_token" not in params:
        if TOKEN:
            params.setdefault("access_token", TOKEN)
        else:
            logger.error("Token not found")

    params.setdefault('v', API_VERSION)


    delay = 0.34 - (time.time() - last_request[0])

    if delay > 0:
        logger.debug(f"sleep {delay}")
        time.sleep(delay)

    response = requests.post(
        URL + method, params, headers=HEADER)
    last_request[0] = time.time()
    response.raise_for_status()
    if list(response.json().keys())[0] == "error":
        raise VkApiError(
            f"VkApiError {response.json()['error']['error_code']} {response.json()['error']['error_msg']}\n{response.json()}"
        )
    return response


