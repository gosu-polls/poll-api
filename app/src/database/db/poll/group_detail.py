from src.database.dbutil.poll_entity import Poll_Entity
import src.database.dba.config as config

class Group_Detail(Poll_Entity):
    _df = {}

    def __new__(cls):
        try:
            # if cls._instance is None:
            hasInstance, cls._instance = cls.HasInstance()
            if not hasInstance:
                cls._df[0] = None
                cls._instance = super(__class__, cls).__new__(cls, 'googlesheet')
                cls._entity_identifier = {'key' : __class__.__module__ + '.' + __class__.__name__,
                                          'pk' : __class__.__name__.lower() + '_id',
                                          'db_type' : 'googlesheet',
                                          'db_name': config.poll_db,
                                          'table_name': __class__.__name__.lower()}
                # cls._filters = {'student_isactive': 'Y'}
            return cls._instance
        except:
            return None
