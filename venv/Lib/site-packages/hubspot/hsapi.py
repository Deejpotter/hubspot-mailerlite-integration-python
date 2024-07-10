class HAPIError(Exception):
    def __init__(self, message, response, code):
        self.value = self.message = message
        self.resposne = response
        self.code = code

    def __str__(self):
        return "{msg} -- HubSpot API responded with: {response} - code {code}".format(
            msg=self.message,
            response=self.response,
            code=self.code
        )

class HSApi:

    def __init__(self, parent):
        self.credentials = parent

    def add_authentication(self, params):
        params[self.credentials.authorization] = self.credentials.auth_value

        return params
