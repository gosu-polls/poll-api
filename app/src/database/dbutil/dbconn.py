from src.database.dba.dbgoogle import GoogleSheet
from src.database.dba.dbcosmos import CosmosDb

class DBConn():
    _dbInstanceMap = {}
    _dbInstance = None
    def __new__(cls, db_type):
        try:
            if db_type not in cls._dbInstanceMap:
                cls._dbInstanceMap[db_type] =  GoogleSheet() if db_type == 'googlesheet' else CosmosDb()
            return cls._dbInstanceMap[db_type]
        except:
            return None
