from app.src.database.dbutil.poll_entity import Poll_Entity

class Vote_Entity(Poll_Entity):
    _pollInstanceMap = {}
    # {poll_id : {
    # cls: instance}}
    _instance = None
    _df = None

    def __new__(cls, db_type, poll_id):
        # if poll_id not in cls._pollInstanceMap:
        print(f"Created [{cls.__name__}] for [{poll_id}]")
        cls._instance = super(__class__, cls).__new__(cls, db_type, poll_id)
        if poll_id not in cls._pollInstanceMap:
            cls._pollInstanceMap[poll_id] = {cls.__name__ : cls._instance}
        else:
            cls._pollInstanceMap[poll_id][cls.__name__] = cls._instance
        
        # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        # print(cls._pollInstanceMap)
        # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

        return cls._pollInstanceMap[poll_id][cls.__name__]
    
    @classmethod
    def GetInstance(cls, poll_id):
        if poll_id in cls._pollInstanceMap:
            if cls.__name__ in cls._pollInstanceMap[poll_id]:
                return cls._pollInstanceMap[poll_id][cls.__name__]

    @classmethod
    def HasInstance(cls, poll_id):
        if poll_id in cls._pollInstanceMap:
            if cls.__name__ in cls._pollInstanceMap[poll_id]:
                # print(f'Found an instance for [{cls.__name__}].[{poll_id}] -> {cls._pollInstanceMap[poll_id][cls.__name__]}')
                return True, cls._pollInstanceMap[poll_id][cls.__name__]
        return False, None
    