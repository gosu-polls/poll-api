from src.database.dbutil.dbconn import DBConn
import pandas as pd
from threading import Lock
read_mutex = Lock()
write_mutex = Lock()

class Poll_Entity:
    _instance = None
    _instanceMap = {}
    _dbInstance = None
    _dbInstanceMap = {}
    _cache = {}
    _db_type = None
    _entity_identifier = {}
    _filters = {}
    _df = None
    # _dfMap = {}
    # _poll_id = 0

    def __new__(cls, db_type, poll_id = 0):
        # cls._dbInstance = DBConn(db_type)
        cls._db_type = db_type
        # cls._dbInstance = DBConn(db_type)
        print(f'Requesting DBConn for {db_type}')
        cls._dbInstanceMap[db_type] = DBConn(db_type)
        try:
            if cls._instance is None or (True if ('instance_per_poll' in cls._entity_identifier and 
                                                  cls._entity_identifier['instance_per_poll'] == 'many')
                                              else False):
                cls._instance = super(__class__, cls).__new__(cls)
                # cls._poll_id = poll_id
                print(f'Created instance for {cls.__name__}.[{poll_id}]')
            return cls._instance
        except Exception as err:
            print(err)
            return None

    @classmethod
    def HasInstance(cls, poll_id = 0) -> bool:
        if cls._instance is not None:
            return True, cls._instance
        return False, None
    
    # @classmethod
    # def HasInstance(cls, poll_id = 0) -> bool:
    #     if cls.__name__ in cls._instanceMap:
    #         return cls._instanceMap[cls.__name__]
    #     else:
    #         return False
    
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
        with read_mutex:
            if not cls._isCached():
                print(f"Priming [{cls._entity_identifier['key']}]")
                cls._df = cls._dbInstanceMap[cls._db_type].ReadData(identifier = cls._entity_identifier,
                                                                    filters = cls._filters)
                
                # cls._dfMap[cls._poll_id] = cls._dbInstanceMap[cls._db_type].ReadData(identifier = cls._entity_identifier,
                                                                    # filters = cls._filters)
                cls._updateCache(cls._entity_identifier['key'])

    @classmethod
    def GetData(cls) -> dict:
        try:
            cls._primeData()
            data = cls._df.to_dict("records")
            # data = cls._dfMap[cls._poll_id].to_dict("records")
            return data
        except Exception as err:
            return {"exception": err}

    @classmethod
    def GetDatum(cls, id) -> dict:
        try:
            cls._primeData()
            data = cls._df[cls._df[cls._entity_identifier['pk'] if 'pk' in cls._entity_identifier else 'id'] == id].to_dict("records")
            return data        
        except Exception as err:
            return {"exception": err}

    @classmethod
    def GetNextId(cls) -> int:
        cls._primeData()
        return 1 if cls._df is None or len(cls._df) == 0 else cls._df[cls._entity_identifier['pk']].max() + 1
    
    @classmethod
    def AddData(cls, data: dict) -> dict:
        new_row = pd.DataFrame(data, index=[0])
        cls._primeData()
        cls._df = pd.concat([cls._df, new_row], ignore_index=True)
        cls.WriteData()
        return cls._df.to_dict("records")

    @classmethod
    def UpdateData(cls, set_clause: dict, where_clause: dict = None) -> dict:
        cls._primeData()
        # Assumption is we have one where clause
        k = ''
        v = ''
        if (len(where_clause) > 0):
            k = list(where_clause.keys())[0]
            v = where_clause[k]
        
        for s in set_clause:
            cls._df.loc[cls._df[k] == v, s] = set_clause[s]
        
        cls.WriteData()

    @classmethod
    def WriteData(cls) -> dict:
        with write_mutex:
            try:
                cls._dbInstanceMap[cls._db_type].WriteData(identifier = cls._entity_identifier, data=cls._df)
            except Exception as err:
                print(err)
                return{"exception": err}

    # @classmethod
    # def _performIO(cls, mode) -> dict:
    #     with mutex:
    #         if mode == 'r':
    #             pass
    #         elif mode == 'w':
    #             pass
    
    @classmethod
    def ResetCache(cls):
        try:
            cls._cache[cls._entity_identifier['key']] = False
            return f"Cache Cleared for [{cls._entity_identifier['key']}]"
        except Exception as err:
            return {"exception": err}

    # @classmethod
    # def _addData(cls, data):
    #     print(cls._entity_identifier)
    #     cls._dbInstanceMap[cls._db_type].AddData(identifier = cls._entity_identifier, data = data)
    #     print(data)
