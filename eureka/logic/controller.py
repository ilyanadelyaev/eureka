class Controller(object):
    """
    Logic controller
    """

    def __init__(self, db_engine):
        self.db_engine = db_engine

    @staticmethod
    def test():
        """
        Test data
        """
        return 'test'
