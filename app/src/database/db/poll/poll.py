from src.database.dbutil.poll_entity import Poll_Entity
import src.database.dba.config as config
from src.database.db.poll.user import User as User
from src.database.db.poll.group import Group as Group
from src.database.db.poll.group_detail import Group_Detail as Group_Detail

from fastapi import Request

class Poll(Poll_Entity):
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
                cls._filters = {'is_active': 'Y'}
            return cls._instance
        except:
            return None

    @classmethod
    def GetAvailablePolls(cls, request: Request) -> list:
        u = User().GetUser(request)
        data = []
        if u != None:
            # data = Poll().GetData()
            data = cls.GetData()
        return data

    @classmethod
    def GetParticipatingPolls(cls, request: Request) -> list:
        u = User().GetUser(request)
        data = []
        if u != None:
            # print(u)
            # For the given email, get the group_id from group_detail
            # For each group_id, get the poll_id from group
            # For each poll_id get poll data from poll
            group_detail = Group_Detail().GetData()
            group = Group().GetData()
            # poll = Poll().GetData()
            poll = cls.GetData()
            data = [p for p in poll if p['poll_id'] in 
                        [g['poll_id'] for g in group if g['group_id'] in 
                            [gd['group_id'] for gd in group_detail if gd['email'] == u['email']]]
                   ]
        return data
    
    @classmethod
    def GetPollObject(cls, request: Request, poll_id: int) -> dict:
        u = User().GetUser(request)
        data = None
        if u != None:
            # poll_data = Poll().GetDatum(poll_id)
            poll_data = cls.GetDatum(poll_id)
            data = poll_data
        return data
    
    @classmethod
    def IsUserAdmin(cls, request: Request, poll_id: int) -> bool:
        u = User().GetUser(request)
        if u!= None:
            poll = cls.GetDatum()
            if poll['admin_user_id'] == u['user_id']:
                return True
        return False