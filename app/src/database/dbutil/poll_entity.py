from app.src.database.dbutil.dbconn import DBConn
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
    _filters = {}
    # _df = None
    _poll_id = 0

    def __new__(cls, db_type, poll_id = 0):
        # cls._dbInstance = DBConn(db_type)
        cls._db_type = db_type
        # cls._dbInstance = DBConn(db_type)
        print(f'Requesting DBConn for {db_type}')
        cls._dbInstanceMap[db_type] = DBConn(db_type)
        try:
            if cls._instance is None or (True if ('instance_per_poll' in cls._entity_identifier[poll_id] and 
                                                  cls._entity_identifier[poll_id]['instance_per_poll'] == 'many')
                                              else False):
                cls._instance = super(__class__, cls).__new__(cls)
                cls._poll_id = poll_id
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
    
    @classmethod
    def _updateCache(cls, key, value = True):
        cls._cache[key] = value

    @classmethod
    def _isCached(cls) -> bool:
        if cls._entity_identifier[cls._poll_id]['key'] not in cls._cache or len(cls._df[cls._poll_id].index) == 0 :
            return False
        else:
            return cls._cache[cls._entity_identifier[cls._poll_id]['key']]

    @classmethod
    def _readData(cls):
        with read_mutex:
            if not cls._isCached():
                # print(f"Priming [{cls.__name__}].[{cls._poll_id}] using [{cls._entity_identifier[cls._poll_id]}]")
                print(f"Priming [{cls.__name__}].[{cls._poll_id}] from [{cls._entity_identifier[cls._poll_id]['db_type']}.{cls._entity_identifier[cls._poll_id]['db_name']}.{cls._entity_identifier[cls._poll_id]['table_name']}]")
                # print(f"Data for [{cls._entity_identifier[cls._poll_id]['key']}] using [{cls._entity_identifier[cls._poll_id]}] before priming {cls._df[cls._poll_id]}")
                # cls._df = cls._dbInstanceMap[cls._db_type].ReadData(identifier = cls._entity_identifier[cls._poll_id],
                #                                                     filters = cls._filters)
                cls._df[cls._poll_id] = cls._dbInstanceMap[cls._db_type].ReadData(identifier = cls._entity_identifier[cls._poll_id],
                                                                    filters = cls._filters)

                # print(f"Data for [{cls._entity_identifier[cls._poll_id]['key']}] using [{cls._entity_identifier[cls._poll_id]}] after priming {cls._df[cls._poll_id]}")
                
                cls._updateCache(cls._entity_identifier[cls._poll_id]['key'])

    @classmethod
    def GetData(cls) -> list:
        try:
            cls._readData()
            # data = cls._df.to_dict("records")
            # print(f"GetData for {cls}.{cls._poll_id} -> {cls._df[cls._poll_id]} ")
            data = cls._df[cls._poll_id].to_dict("records")
            # print(f"poll_entity -> GetData for {cls._entity_identifier[cls._poll_id]['table_name']} is {data}")            
            return data
        except Exception as err:
            print(str(err))
            return {"exception": err}

    @classmethod
    def GetDatum(cls, id) -> dict:
        try:
            data : {}
            cls._readData()
            # data = cls._df[cls._df[cls._entity_identifier[cls._poll_id]['pk'] if 'pk' in cls._entity_identifier[cls._poll_id] else 'id'] == id].to_dict("records")
            df = cls._df[cls._poll_id]
            data = df[df[cls._entity_identifier[cls._poll_id]['pk'] if 'pk' in cls._entity_identifier[cls._poll_id] else 'id'] == id].to_dict("records")
            if len(data) > 0:
                return data[0]
            return data
        except Exception as err:
            return {"exception": err}

    @classmethod
    def GetFilteredData(cls, where_clause : dict) -> list:
        try:
            data = []
            # Assumption is that the where clause will have only one filter
            k = list(where_clause.keys())[0]
            v = where_clause[k]
            cls._readData()
            df = cls._df[cls._poll_id].loc[cls._df[cls._poll_id][k] == v]
            data = df.to_dict("records")
            return data
        except Exception as err:
            return {"exception": err}

    @classmethod
    def _getNextId(cls) -> int:
        cls._readData()
        # return 1 if cls._df is None or len(cls._df) == 0 else cls._df[cls._entity_identifier[cls._poll_id]['pk']].max() + 1
        return 1 if cls._df[cls._poll_id] is None or len(cls._df[cls._poll_id]) == 0 else cls._df[cls._poll_id][cls._entity_identifier[cls._poll_id]['pk']].max() + 1
    
    @classmethod
    # mode: 
    #   - a (append)
    #   - u (update)
    #   - w (write)
    # body:
    #   - data
    #   - set_clause
    #   - where_clause
    def _writeData(cls, mode : str, body: dict):
        with write_mutex:
            data = []
            try:
                if mode in ['a', 'u']:
                    cls._readData()
                    # print(f'_writeData existing data is {cls._df[cls._poll_id]}')
                    # print(f'cls._entity_identifier[cls._poll_id] is {cls._entity_identifier[cls._poll_id]}')
                    if mode == 'a':
                        data = body['data']
                        pk = cls._getNextId()
                        data[cls._entity_identifier[cls._poll_id]['pk']] = pk
                        new_row = pd.DataFrame(data, index=[0])
                        cls._df[cls._poll_id] = pd.concat([cls._df[cls._poll_id], new_row], ignore_index=True)
                        data = [pk]
                    elif mode == 'u':
                        # print(f"_writeData printing body -> {body['block_data_df']}")
                        # if len(body['block_data_df'].index) > 0:
                        if body['block_data_df'] is not None:
                            # print(f'_write_data before {cls._df[cls._poll_id]}')
                            cls._df[cls._poll_id].set_index(cls._entity_identifier[cls._poll_id]['pk'] if 'pk' in cls._entity_identifier[cls._poll_id] else 'id', inplace = True)
                            cls._df[cls._poll_id].update(body['block_data_df'].set_index(cls._entity_identifier[cls._poll_id]['pk'] if 'pk' in cls._entity_identifier[cls._poll_id] else 'id'))
                            cls._df[cls._poll_id].reset_index(inplace = True)
                            # print(f'_write_data after {cls._df[cls._poll_id]}')
                        else:
                            # Assumption is we have one where clause
                            k = ''
                            v = ''
                            if (len(body['where_clause']) > 0):
                                k = list(body['where_clause'].keys())[0]
                                v = body['where_clause'][k]
                        
                            for s in body['set_clause']:
                                # cls._df.loc[cls._df[k] == v, s] = set_clause[s]
                                cls._df[cls._poll_id].loc[cls._df[cls._poll_id][k] == v, s] = body['set_clause'][s]

                cls._dbInstanceMap[cls._db_type].WriteData(identifier = cls._entity_identifier[cls._poll_id], data=cls._df[cls._poll_id])
                return data
            except Exception as err:
                print(err)
                return{"exception": err}

    @classmethod
    def AddData(cls, data: dict) -> dict:
        body = {'data': data}
        return cls._writeData(mode='a', body=body)

        # new_row = pd.DataFrame(data, index=[0])
        # cls._readData()
        # cls._df[cls._poll_id] = pd.concat([cls._df[cls._poll_id], new_row], ignore_index=True)
        # cls.WriteData()
        
        # return cls._df[cls._poll_id].to_dict("records")

    @classmethod
    def UpdateData(cls, set_clause: dict = None, where_clause: dict = None, block_data_df: list = None) -> dict:
        body = {
                    'set_clause': set_clause,
                    'where_clause': where_clause,
                    'block_data_df' : block_data_df
               }
        
        # print(f'UpdateData -> body {body}')
        cls._writeData(mode='u', body=body)
        
        # cls._readData()
        # # Assumption is we have one where clause
        # k = ''
        # v = ''
        # if (len(where_clause) > 0):
        #     k = list(where_clause.keys())[0]
        #     v = where_clause[k]
        
        # for s in set_clause:
        #     # cls._df.loc[cls._df[k] == v, s] = set_clause[s]
        #     cls._df[cls._poll_id].loc[cls._df[cls._poll_id][k] == v, s] = set_clause[s]
        
        # cls.WriteData()

    @classmethod
    def UpsertData(cls, set_clause: dict, where_clause: dict = None) -> dict:
        pass
    # @classmethod
    # def WriteData(cls) -> dict:
    #     with write_mutex:
    #         try:
    #             cls._dbInstanceMap[cls._db_type].WriteData(identifier = cls._entity_identifier[cls._poll_id], data=cls._df[cls._poll_id])
    #         except Exception as err:
    #             print(err)
    #             return{"exception": err}

    @classmethod
    def ResetCache(cls):
        try:
            cls._cache[cls._entity_identifier[cls._poll_id]['key']] = False
            cls._readData()
            # cls._cache = {}
            # return f"Cache Cleared for [{cls._entity_identifier[cls._poll_id]['key']}]"
        except Exception as err:
            return {"exception": err}

    # @classmethod
    # def _addData(cls, data):
    #     print(cls._entity_identifier[cls._poll_id])
    #     cls._dbInstanceMap[cls._db_type].AddData(identifier = cls._entity_identifier[cls._poll_id], data = data)
    #     print(data)
