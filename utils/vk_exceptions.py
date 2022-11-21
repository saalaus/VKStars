class VkApiError(Exception):
    def __init__(self, response, params, func_method):
        error = response.get("error", {})
        self.error_code = error.get("error_code")
        self.error_msg = error.get("error_msg")
        self.critical = error.get("critical")
        self.params = params
        self.func_method = func_method
        self.method = None
        self.oauth = None
        for params in error.get("request_params", {}):
            setattr(self, params["key"], params["value"])

    def __str__(self) -> str:
        if self.error_msg:
            return f"Api call error [{self.error_code}]: {self.error_msg}"
        return "Undefined api call error"
    
    def try_again(self, **new_params):
        new_params.update(self.params)
        return self.func_method(self.method, **new_params)
