class LogicError(Exception):
    pass


class InvalidArgument(LogicError):
    def __init__(self, arg, val):
        super(InvalidArgument, self).__init__(
            'Invalid argument "{}": "{}"'.format(
                arg, val if val else ':empty:'))
