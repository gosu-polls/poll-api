from src.database.db.entity import Entity
import src.database.dba.config as config
from fastapi import Request
import json
import jwt

class User(Entity):

    def __new__(cls):
        try:
            if cls._instance is None:
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

    def GetUser(cls, request: Request) -> dict:
        header = json.loads(request.headers.get('Token'))
        user = None
        if header != None:
            
            email = jwt.decode(header['jwt'], 'secret', 'HS256')['email']

            users = cls.GetData()
            userList = [u for u in users if u['email'] == email]
            user = userList[0]

        return user