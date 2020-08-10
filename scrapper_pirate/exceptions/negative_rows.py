class NegativeRowsException(Exception):
    """
    Exception raised for errors in the input rows to scrap

    Attributes:
        rows_to_scrap -- input row which caused the error
        message -- explanation about the error
    """

    def __init__(self, rows_to_scrap, message='The size of rows_to_scrap is less than zero'):
        self.rows_to_scrap = rows_to_scrap
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.rows_to_scrap} -> {self.message}'
