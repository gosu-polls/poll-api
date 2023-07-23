from src.db.entity import Entity
import src.dba.config as config

class Group(Entity):

    def __new__(cls):
        try:
            if cls._instance is None:
                cls._instance = super(__class__, cls).__new__(cls, 'googlesheet')
                cls._entity_identifier = {'key' : __class__.__module__ + '.' + __class__.__name__,
                                          'pk' : __class__.__name__.lower() + '_id',
                                          'db_type' : 'googlesheet',
                                          'db_name': config.poll_db,
                                          'table_name': 'group'}
                # cls._filters = {'student_isactive': 'Y'}
            return cls._instance
        except:
            return None