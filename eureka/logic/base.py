class ManagerBase(object):
    """
    Manager base
    """

    def __init__(self, db_engine):
        self.db_engine = db_engine
