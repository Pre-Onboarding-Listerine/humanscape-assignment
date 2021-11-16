class UnauthorizedAuthenticationKeyException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class OpenAPIServerErrorException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class DoesNotExistTrialsException(Exception):
    pass


class DuplicatedTrialsException(Exception):
    pass


class TrialNotFoundException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
