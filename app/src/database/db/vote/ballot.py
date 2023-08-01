from src.database.dbutil.vote_entity import Vote_Entity
from src.database.dbutil.poll_object import Poll_Object

class Ballot(Vote_Entity):

    def __new__(cls, poll_object: Poll_Object):
        try:
            # if not cls.HasInstance(poll_object.poll_id):
            hasInstance, cls._instance = cls.HasInstance(poll_object.poll_id)
            if not hasInstance:
                print(f"Creating [{__class__.__name__}] for [{poll_object.poll_id}]")
                cls._entity_identifier = {'key' : __class__.__module__ + '.' + __class__.__name__ + '_[' + str(poll_object.poll_id) + ']',
                                          'pk' : __class__.__name__.lower() + '_id',
                                          'db_type' : 'googlesheet',
                                          'db_name': poll_object.connection_string,
                                          'table_name': __class__.__name__.lower(),
                                          'instance_per_poll' : 'many'}
                cls._instance = super(__class__, cls).__new__(cls, 'googlesheet', poll_object.poll_id)
                # cls._filters = {'student_isactive': 'Y'}
            return cls._instance
        except:
            return None
