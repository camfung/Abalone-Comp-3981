
class DuplicateSingletons(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidMarbleValue(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidDirection(Exception):
    def __init__(self, message):
        super().__init__(message)
