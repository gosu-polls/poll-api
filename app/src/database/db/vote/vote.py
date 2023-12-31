from app.src.database.dbutil.vote_entity import Vote_Entity
from app.src.database.dbutil.poll_object import Poll_Object
from app.src.database.db.poll.user import User as User

class Vote(Vote_Entity):
    _df = {}
    _entity_identifier = {}
    _poll_id = None

    def __new__(cls, poll_object: Poll_Object):
        try:
            hasInstance, cls._instance = cls.HasInstance(poll_object.poll_id)
            cls._poll_id = poll_object.poll_id
            if not hasInstance:
                cls._df[poll_object.poll_id] = None
                print(f"Creating [{__class__.__name__}] for [{poll_object.poll_id}]")
                cls._entity_identifier[poll_object.poll_id] = {'key' : __class__.__module__ + '.' + __class__.__name__ + '_[' + str(poll_object.poll_id) + ']',
                                                               'pk' : __class__.__name__.lower() + '_id',
                                                               'db_type' : 'googlesheet',
                                                               'db_name': poll_object.connection_string,
                                                               'table_name': __class__.__name__.lower(),
                                                               'instance_per_poll' : 'many'}
                cls._instance = super(__class__, cls).__new__(cls, 'googlesheet', poll_object.poll_id)
                # cls._filters = {'student_isactive': 'Y'}
                
            return cls._instance
        except Exception as err:
            print(str(err))
            return None

    @classmethod
    def IsVoteActive(cls, vote_id: int) -> bool:
        vote = cls.GetDatum(vote_id)
        is_open = vote['is_open']
        if is_open.strip() == '':
            is_open = 'Y'
        return True if is_open.upper() == 'Y' else False
        

    @classmethod
    def GetClosedVotes(cls) -> list:
        data = None
        data = cls.GetFilteredData({'is_open' : 'N'})
        # print(f'GetClosedVotes -> {data}')
        return data