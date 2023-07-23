from src.dbutil.dbconn import DBConn
import pandas as pd
class Entity:
    _instance = None
    _dbInstance = None
    _dbInstanceMap = {}
    _cache = {}
    _db_type = None
    _entity_identifier = {}
    _filters = {}
    _df = None

    def __new__(cls, db_type):
        # cls._dbInstance = DBConn(db_type)
        cls._db_type = db_type
        cls._dbInstance = DBConn(db_type)
        cls._dbInstanceMap[db_type] = DBConn(db_type)
        try:
            if cls._instance is None:
                cls._instance = super(__class__, cls).__new__(cls)
            
            # print(f'Entity {cls._instance}')
            return cls._instance
        except:
            return None

    @classmethod
    def _updateCache(cls, key, value = True):
        cls._cache[key] = value

    @classmethod
    def _isCached(cls) -> bool:
        if cls._entity_identifier['key'] in cls._cache:
            return cls._cache[cls._entity_identifier['key']]
        else:
            return False

    @classmethod
    def _primeData(cls):
        print(f"Priming [{cls._entity_identifier['key']}]")
        cls._df = cls._dbInstanceMap[cls._db_type].ReadData(identifier = cls._entity_identifier,
                                                            filters = cls._filters)
        
        # print(f'Primed Data: {type(cls._df)}')
        cls._updateCache(cls._entity_identifier['key'])

    @classmethod
    def GetData(cls) -> dict:
        try:
            if not cls._isCached():
                cls._primeData()
            # print(f'Cached Data: {type(cls._df)}')
            return cls._df.to_dict("records")
        except Exception as err:
            return {"exception": err}

    @classmethod
    def GetDatum(cls, id) -> dict:
        try:
            if not cls._isCached():
                cls._primeData()
            return cls._df[cls._df[cls._entity_identifier['pk'] if 'pk' in cls._entity_identifier else 'id'] == id].to_dict("records")
        except Exception as err:
            return {"exception": err}

    @classmethod
    def GetNextId(cls) -> int:
        return cls._df[cls._entity_identifier['pk']].max() + 1
    
    @classmethod
    def AppendData(cls, data: dict) -> dict:
        new_row = pd.DataFrame(data, index=[0])
        # print(new_row)
        cls._df = pd.concat([cls._df, new_row], ignore_index=True)
        print(f'appended data is {cls._df}')
        cls.WriteData()

    @classmethod
    def WriteData(cls) -> dict:
        try:
            cls._dbInstanceMap[cls._db_type].WriteData(identifier = cls._entity_identifier, data=cls._df)
        except Exception as err:
            print(err)
            return{"exception": err}

    @classmethod
    def ResetCache(cls):
        try:
            cls._cache[cls._entity_identifier['key']] = False
            return f"Cache Cleared for [{cls._entity_identifier['key']}]"
        except Exception as err:
            return {"exception": err}

    @classmethod
    def _addData(cls, data):
        print(cls._entity_identifier)
        cls._dbInstanceMap[cls._db_type].AddData(identifier = cls._entity_identifier, data = data)
        print(data)
