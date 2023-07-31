from src.database.dbutil.entity import Entity
# from src.module.poll_object import Poll_Object as Poll_Object

class Vote_Main(Entity):
    _pollInstanceMap = {}
    _instance = None

    def __new__(cls, db_type, poll_id):
        # if poll_id not in cls._pollInstanceMap:
        cls._instance = super(__class__, cls).__new__(cls, db_type)
        cls._pollInstanceMap[poll_id] = cls._instance
        return cls._pollInstanceMap[poll_id]
    

    @classmethod
    def HasInstance(cls, poll_id) -> bool:
        
        if poll_id in cls._pollInstanceMap:
            return cls._pollInstanceMap[poll_id]
        return False