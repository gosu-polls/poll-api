from src.dbutil.dbconn import DBConn

class Entity:
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
        
        cls._updateCache(cls._entity_identifier['key'])

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
