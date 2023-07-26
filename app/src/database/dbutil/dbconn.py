from src.database.dba.dbgoogle import GoogleSheet
from src.database.dba.dbcosmos import CosmosDb
from threading import Lock
mutex = Lock()

class DBConn():
    _dbInstanceMap = {}
    _dbInstance = None
    def __new__(cls, db_type):
        try:
            with mutex:
                if db_type not in cls._dbInstanceMap:
                    print(f'Making DBConn for {db_type}')
                    cls._dbInstanceMap[db_type] =  GoogleSheet() if db_type == 'googlesheet' else CosmosDb()
                return cls._dbInstanceMap[db_type]
        except:
            return None
