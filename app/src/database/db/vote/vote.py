from src.database.dbutil.vote_main import Vote_Main
import src.database.dba.config as config
from src.module.poll_object import Poll_Object as Poll_Object

class Vote(Vote_Main):

    def __new__(cls, poll_object: Poll_Object):
        try:
            if not cls.HasInstance(poll_object.poll_id):
                # print(f"Creating {__class__.__module__ + '.' + __class__.__name__ } instance for {poll_object.poll_name}")
                cls._instance = super(__class__, cls).__new__(cls, 'googlesheet', poll_object.poll_id)
                cls._entity_identifier = {'key' : __class__.__module__ + '.' + __class__.__name__ + '_[' + str(poll_object.poll_id) + ']',
                                          'pk' : __class__.__name__.lower() + '_id',
                                          'db_type' : 'googlesheet',
                                          'db_name': poll_object.connection_string,
                                          'table_name': __class__.__name__.lower()}
                # cls._filters = {'student_isactive': 'Y'}
            return cls._instance
        except:
            return None
