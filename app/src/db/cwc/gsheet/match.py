from src.db.entity import Entity
import src.db.cwc.gsheet.config as config

class Match(Entity):
    _instance = None
    _df = None

    def __new__(cls):
        try:
            if cls._instance is None:
                cls._instance = super(__class__, cls).__new__(cls, 'googlesheet')
                cls._entity_identifier = {'key' : __class__.__module__ + '.' + __class__.__name__,
                                          'db_type' : 'googlesheet',
                                          'db_name': config.cwc_static,
                                          'table_name': 'match'}
                # cls._filters = {'student_isactive': 'Y'}
            return cls._instance
        except:
            return None

    @classmethod
    def GetMatches(cls) -> dict():
        try:
            if not cls._isCached():
                cls._primeData()
            return cls._df.to_dict("records")
        except Exception as err:
            return {"exception": err}

    @classmethod
    def GetMatch(cls, id) -> dict():
        try:
            if not cls._isCached():
                cls._primeData()
            return cls._df[cls._df['match_id'] == id].to_dict("records")
        except Exception as err:
            return {"exception": err}