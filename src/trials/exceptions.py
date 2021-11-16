class UnauthorizedAuthenticationKeyException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class OpenAPIServerErrorException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
