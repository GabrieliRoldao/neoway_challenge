class ArgsOutRangeException(Exception):
    """
    Exception raised when pass to much args to main function

    Attributes:
        args -- input args which caused the error
        message -- explanation about the error
    """

    def __init__(self, args, message='Error with input args'):
        self.args = args
        self.size = len(args)
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}\nArgs out of range, passed more than two args. Limit of args is 2, got {self.size}.'
