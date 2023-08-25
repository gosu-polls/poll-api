from app.src.database.dbutil.poll_entity import Poll_Entity

class Country(Poll_Entity):
    _instance = None
    _df = None

    def __new__(cls):
        try:
            if cls._instance is None:
                cls._instance = super(__class__, cls).__new__(cls, 'cosmosdb')
                cls._entity_identifier = {'key' : __class__.__module__ + '.' + __class__.__name__,
                                          'db_type' : 'cosmosdb',
                                          'container_name' : 'cwc',
                                          'partition_key': 'country',
                                          'item_name' : 'country'}
            return cls._instance
        except:
            return None
        
    @classmethod
    def GetCountries(cls) -> dict():
        try:
            if not cls._isCached():
                cls._primeData()
            return cls._df.to_dict("records")
        except Exception as err:
            return {"exception": err}

    @classmethod
    def GetCountry(cls, id) -> dict():
        try:
            if not cls._isCached():
                cls._primeData()
            return cls._df[cls._df['country_id'] == id].to_dict("records")
        except Exception as err:
            return {"exception": err}