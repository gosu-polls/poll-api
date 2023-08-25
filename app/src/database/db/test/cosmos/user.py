from src.database.dbutil.poll_entity import Poll_Entity
import os

class User(Poll_Entity):
    _instance = None
    _df = None

    def __new__(cls):
        try:
            if cls._instance is None:
                cls._instance = super(__class__, cls).__new__(cls, 'cosmosdb')
                cls._entity_identifier = {'key' : __class__.__module__ + '.' + __class__.__name__,
                                          'item_identifier' : __class__.__name__.lower(),
                                          'db_type' : 'cosmosdb',
                                          'container_name' : os.getenv('COSMOSDB_CWC_CONTAINER_ID'),
                                          'partition_key': 'email'
                                          }
            return cls._instance
        except:
            return None

    @classmethod
    def GetUsers(cls) -> dict():
        try:
            if not cls._isCached():
                cls._primeData()
            return cls._df.to_dict("records")
        except Exception as err:
            return {"exception": err}

    @classmethod
    def GetUser(cls, id) -> dict():
        try:
            if not cls._isCached():
                cls._primeData()
            return cls._df[cls._df['user_id'] == id].to_dict("records")
        except Exception as err:
            return {"exception": err}
        
    @classmethod
    def AddUser(cls, user) -> dict():
        try:
            cls._addData(user)
        except Exception as err:
            return {"exception": err}