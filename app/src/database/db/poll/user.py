from src.database.dbutil.poll_entity import Poll_Entity
import src.database.dba.config as config
from fastapi import Request
import json
import jwt

class User(Poll_Entity):
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
    def GetUser(cls, request: Request) -> dict:
        header = json.loads(request.headers.get('Token'))
        user = None
        if header != None:
            
            email = jwt.decode(header['jwt'], 'secret', 'HS256')['email']

            users = cls.GetData()
            # print(f'user.GetUser users {users}')

            userList = [u for u in users if u['email'] == email]
            # print(f'user.GetUser userList {userList}')
            user = userList[0]

        return user