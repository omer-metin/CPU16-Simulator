class NotAllowedError(Exception):

    # STATIC VARIABLES #

    # DUNDERS #
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "operation is not allowed"

    # PROPERTIES #

    # PUBLIC METHODS #

    # PRIVATE METHODS #


class SetOpNotAllowedError(NotAllowedError):

    # STATIC VARIABLES #

    # DUNDERS #
    def __str__(self):
        return "set " + super().__str__()

    # PROPERTIES #

    # PUBLIC METHODS #

    # PRIVATE METHODS #
