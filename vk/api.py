import time

import requests
from loader import config, logger
from utils.vk_exceptions import VkApiError

URL = 'https://api.vk.com/method/'
HEADER = {
    'user-agent': "VKAndroidApp/5.23-2978 (Android 4.4.2; SDK 19; x86; unknown Android SDK built for x86; en; 320x240)"}


def method(method_name: str, **params):
    """main function to call VK methods

    @param method_name: str: method name
    @param params: method option

    """
    if "access_token" not in params:
        params.setdefault("access_token", config.user_token)
    params.setdefault('v', config.api_version)

    delay = 0.34 - (time.time() - config.last_request)

    if delay > 0:
        logger.debug(f"sleep {delay}")
        time.sleep(delay)

    #logger.debug(f"Method {method_name} with params {params}")
    response = requests.post(
        URL + method_name, params, headers=HEADER).json()

    config.last_request = time.time()

    if "error" in response:
        raise VkApiError(response, params, method)

    return response


