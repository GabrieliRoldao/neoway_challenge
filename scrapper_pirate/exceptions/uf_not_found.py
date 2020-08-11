class UfNotFound(Exception):
    """
    Exception raised for errors in the UF input

    Attributes:
        uf -- uf input which caused the error
        message -- explanation about the error
    """

    def __init__(self, uf, message='UF not found at the Correios API'):
        self.uf = uf
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}. UF requested: {self.uf}'
