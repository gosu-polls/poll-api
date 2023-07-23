import functools
import json
import jwt
from fastapi import Request
from src.db.poll.gsheet.group import Group as Group
from src.db.poll.gsheet.poll import Poll as Poll
import src.user as user
import uuid
class polls():
    def init():
        pass

def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # print("******************************************")
        request = args[0]
        # print(f"poll.login_required args -> {request}")
        # print(f"poll.login_required kwargs -> {kwargs}")
        # print("******************************************")
        header = ''
        header = json.loads(request.headers.get('Token'))
        # print(header)
        if header == None:
            # print('None')
            # return None
            return func(*args, **kwargs)
        else:
            # print(jwt.decode(header['jwt'], 'secret', 'HS256')['email'])
            return func(*args, **kwargs)
    return wrapper

def get_available_polls(request: Request) -> dict:
    u = user.get_user(request)
    data = []
    if u != None:
        data = Poll().GetData()
    return {'data': data}

# def _get_groups()-> dict:
#     data = Group().GetData()
#     return data

def get_groups_admin(request: Request) -> dict:
    u = user.get_user(request)
    data = []
    if u != None:
        groups = Group().GetData()
        header = json.loads(request.headers.get('Token'))
        if header != None:
            email = jwt.decode(header['jwt'], 'secret', 'HS256')['email']
            data = [g for g in groups if g['group_admin'] == email]

    return {'data': data}

def create_group(request: Request, body: dict) -> dict:
    u = user.get_user(request)
    data = []
    if u != None:
        groups = Group().GetData()
        # print(groups)
        # print(f'body is {body}')
        # print(body['group_name'])
        # [{'group_id': 1, 'group_name': 'bunch', 'group_code': '', 'group_admin': 'kirankumar.gosu@gmail.com'}, 
        #  {'group_id': 2, 'group_name': 'mrit', 'group_code': '', 'group_admin': 'jamozhi08@gmail.com'}]

        # {'available_poll': {'id': 122, 'poll_name': 'CWC'}, 'group_name': 'm'}
        if (body['group_name'] in [g['group_name'] for g in groups if g['group_admin'] == u]):
            data.append('Group Name already exists')
        else:
            group_code = uuid.uuid4().hex
            new_group = {'group_id': Group().GetNextId(),
                         'group_name': body['group_name'],
                         'group_code': group_code,
                         'group_admin': u['email'],
                         'poll_id': body['available_poll']['poll_id']
                        }
            # print(new_group)
            Group().AppendData(new_group)
            # Group().WriteData()
        # if body['group_name'] in [g]
    return {'data': data}

def get_active_poll(request: Request) -> dict:
    u = user.get_user(request)
    data = {}
    if u != None:
        
        data = {'poll_no' : 4,
                'question' : 'India vs Australia',
                'options' : [
                             {'id': 0,
                              'opt': 'India'}, 
                             {'id': 1,
                              'opt': 'Australia'},
                             {'id': 2,
                              'opt': 'NR / Tie'}
                            ]
               }
    return {'data': data}
    
def get_poll_history(request: Request) -> dict:
    u = user.get_user(request)
    if u != None:
        return {'data' : 
                    {"history" : [
                                    {'id': 0,
                                     'question' : 'ENG vs NZL',
                                     'options' : {'England' : [{'email': 'kirankumar.gosu@gmail.com',
                                                                'initials': 'KG'},
                                                               {'email': 'sivapragasam.m@gmail.com',
                                                                'initials': 'SM'},
                                                               {'email': 'arunmozhidevan.g@gmail.com',
                                                                'initials': 'AG'}],
                                                  'New Zeleand': [{'email': 'suresh.nalikela@gmail.com',
                                                                  'initials': 'SN'},
                                                                  {'email': 'rasheed.abdur@gmail.com',
                                                                   'initials': 'RA'}],
                                                  'NR / Tie' : []
                                                 },
                                     'right' : 'England'
                                     },
                                     {'id': 1,
                                      'question' : 'NED vs PAK',
                                      'options' : {'Netherlands' : [{'email': 'sivapragasam.m@gmail.com',
                                                                'initials': 'SM'},
                                                               {'email': 'arunmozhidevan.g@gmail.com',
                                                                'initials': 'AG'}],
                                                  'Pakistan': [{'email': 'kirankumar.gosu@gmail.com',
                                                                   'initials': 'KG'},
                                                                  {'email': 'suresh.nalikela@gmail.com',
                                                                   'initials': 'SN'},
                                                                  {'email': 'rasheed.abdur@gmail.com',
                                                                   'initials': 'RA'}],
                                                  'NR / Tie' : []
                                                 },
                                     'right' : 'Netherlands'
                                     },
                                     {'id': 2,
                                     'question' : 'AFG vs BAN',
                                     'options' : {'Afghanistan' : [{'email': 'sivapragasam.m@gmail.com',
                                                                'initials': 'SM'},
                                                               {'email': 'arunmozhidevan.g@gmail.com',
                                                                'initials': 'AG'}],
                                                  'Bangladesh': [{'email': 'kirankumar.gosu@gmail.com',
                                                                   'initials': 'KG'},
                                                                  {'email': 'suresh.nalikela@gmail.com',
                                                                   'initials': 'SN'},
                                                                  {'email': 'rasheed.abdur@gmail.com',
                                                                   'initials': 'RA'}],
                                                  'NR / Tie' : []
                                                 },
                                     'right' : 'Afghanistan'
                                     },
                                     {'id': 3,
                                     'question' : 'RSA vs SRI',
                                     'options' : {'South Africa' : [{'email': 'sivapragasam.m@gmail.com',
                                                                'initials': 'SM'},
                                                               {'email': 'arunmozhidevan.g@gmail.com',
                                                                'initials': 'AG'}],
                                                  'Sri Lanka': [{'email': 'kirankumar.gosu@gmail.com',
                                                                   'initials': 'KG'},
                                                                  {'email': 'suresh.nalikela@gmail.com',
                                                                   'initials': 'SN'},
                                                                  {'email': 'rasheed.abdur@gmail.com',
                                                                   'initials': 'RA'}],
                                                  'NR / Tie' : []
                                                 },
                                     'right' : 'South Africa'
                                     }
                                 ]
                    } 
               }
    else:
        return {'data': {}}