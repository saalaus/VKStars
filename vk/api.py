import time
from typing import Any

import requests
from data import settings
from utils.vk_exceptions import VkApiError

URL = 'https://api.vk.com/method/'
last_request = [0.0]


def method(method_name: str, **params: Any) -> dict[Any, Any]:
    """main function to call VK methods

    @param method_name: str: method name
    @param params: method option

    """
    logger.debug(f"Method {method_name} with params {params}")

    if "access_token" not in params:
        params.setdefault("access_token", settings.USER_TOKEN)
    params.setdefault('v', settings.API_VERSION)

    delay = 0.34 - (time.time() - last_request[0])

    if delay > 0:
        logger.debug(f"sleep {delay}")
        time.sleep(delay)

    response = requests.post(URL + method_name, params).json()

    last_request[0] = time.time()

    if "error" in response:
        raise VkApiError(response, params, method)
    return response

