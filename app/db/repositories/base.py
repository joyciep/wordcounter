class BaseRepository(object):
    def __init__(self, db_session):
        self.db_session = db_session
