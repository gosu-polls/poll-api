from src.database.dbutil.vote_entity import Vote_Entity
from src.database.dbutil.poll_object import Poll_Object
from src.database.db.poll.user import User as User
from fastapi import Request

class Ballot(Vote_Entity):
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
        except:
            return None

    @classmethod
    def GetUserBallot(cls, request: Request) -> list:
        u = User().GetUser(request)
        data = []
        if u != None:
            ballot = cls.GetData()
            data = [b for b in ballot if b['user_id'] == u['user_id']]
            # print(data)
        return data

    @classmethod
    def GetUserVoteDetail(cls, request: Request, vote_id: int) -> int:
        u = User().GetUser(request)
        data = []
        if u != None:
            ballot = cls.GetData()
            # print(f'GetUserVoteDetail ballot raw data {ballot}')
            ballot_data = [b for b in ballot if b['user_id'] == u['user_id'] and 
                                                b['vote_id'] == vote_id]
            if len(ballot_data) > 0:
                data = ballot_data[0]
            # print(f'GetUserVoteDetail ballot returning data {data}')
        return data
    
    @classmethod
    def GetVoteDetailAllUsers(cls, request: Request) -> list:
        u = User().GetUser(request)
        data = []
        if u != None:
            ballot = cls.GetData()
            user_data = User().GetData()
            for b in ballot:
                b['user_data'] = [u for u in user_data if u['user_id'] == b['user_id']]
            print(f'GetVoteDetailAllUsers: ballot data with user info {ballot}')
            data = ballot
        return data