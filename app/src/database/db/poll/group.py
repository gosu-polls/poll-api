from app.src.database.dbutil.poll_entity import Poll_Entity
import app.src.database.dba.config as config
from app.src.database.db.poll.user import User as User
from app.src.database.db.poll.group_detail import Group_Detail as Group_Detail

class Group(Poll_Entity):
    _df = {}
    _entity_identifier = {}

    def __new__(cls):
        try:
            # if cls._instance is None:
            hasInstance, cls._instance = cls.HasInstance()
            if not hasInstance:
                cls._df[0] = None
                cls._instance = super(__class__, cls).__new__(cls, 'googlesheet')
                cls._entity_identifier[0] = {'key' : __class__.__module__ + '.' + __class__.__name__,
                                             'pk' : __class__.__name__.lower() + '_id',
                                             'db_type' : 'googlesheet',
                                             'db_name': config.poll_db,
                                             'table_name': __class__.__name__.lower()}
                # cls._filters = {'student_isactive': 'Y'}
            return cls._instance
        except:
            return None

    @classmethod
    def GetGroups(cls, u: User) -> list:
        data = []
        if u != None:
            # For the given email, get the group_id from group_detail
            # For each group_id, get group
            group_detail = Group_Detail().GetData()
            group = Group().GetData()
            data = [g for g in group if g['group_id'] in 
                        [gd['group_id'] for gd in group_detail if gd['email'] == u['email']]
                   ]
        return data
    
    # @classmethod
    # def GetGroups(cls, email: str) -> list:
    #     # For the given email, get the group_id from group_detail
    #     # For each group_id, get group
    #     group_detail = Group_Detail().GetData()
    #     group = Group().GetData()
    #     data = [g for g in group if g['group_id'] in 
    #                 [gd['group_id'] for gd in group_detail if gd['email'] == email]
    #            ]
    #     return data
    
    @classmethod
    def GetAdminGroups(cls, u: User) -> list:
        data = []
        if u != None:
            groups = Group().GetData()
            data = [g for g in groups if g['group_admin'] == u['email']]
        return data
    
    # @classmethod
    # def GetAdminGroups(cls, email: str) -> list:
    #     groups = Group().GetData()
    #     data = [g for g in groups if g['group_admin'] == email]
    #     return data
    
