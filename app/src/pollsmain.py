import functools
import json
import jwt
from fastapi import Request
from src.database.db.poll.gsheet.group import Group as Group
from src.database.db.poll.gsheet.group_detail import Group_Detail as Group_Detail
from src.database.db.poll.gsheet.poll import Poll as Poll
from src.database.db.poll.gsheet.user import User as User
# import src.user as user
import uuid
from datetime import datetime

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
    # u = user.get_user(request)
    u = User().GetUser(request)
    data = []
    if u != None:
        data = Poll().GetData()
    return {'data': data}

def _get_my_groups(request: Request) -> list:
    # u = user.get_user(request)
    u = User().GetUser(request)
    data = []
    if u != None:
        groups = Group().GetData()
        header = json.loads(request.headers.get('Token'))
        if header != None:
            email = jwt.decode(header['jwt'], 'secret', 'HS256')['email']
            data = [g for g in groups if g['group_admin'] == email]

    return data

def get_groups_admin(request: Request) -> dict:
    # u = user.get_user(request)
    u = User().GetUser(request)
    data = []
    if u != None:
        data = _get_my_groups(request)

    return {'data': data}

def create_group(request: Request, body: dict) -> dict:
    # u = user.get_user(request)
    u = User().GetUser(request)
    data = []
    if u != None:
        # print(u)
        groups = Group().GetData()
        if (body['group_name'] in [g['group_name'] for g in groups if g['group_admin'] == u['email']]):
            print('Group already exists')
            data.append('Group already exists')
        else:
            group_code = uuid.uuid4().hex
            group_id = Group().GetNextId()
            new_group = {'group_id': group_id,
                         'group_name': body['group_name'],
                         'group_code': group_code,
                         'group_admin': u['email'],
                         'poll_id': body['available_poll']['poll_id']
                        }
            Group().AddData(new_group)
            group_detail_id = Group_Detail().GetNextId()
            # group_detail_id	group_id	email	joined_on
            new_group_detail = {'group_detail_id' : group_detail_id,
                                'group_id': group_id,
                                'email': u['email'],
                                'joined_on': datetime.now().strftime("%Y-%m-%d %H%M%S")
                                }
            Group_Detail().AddData(new_group_detail)
            data = _get_my_groups(request)
            # data.append('Group Created')
            
    return {'data': data}

def join_group(request: Request, body: dict) -> dict:
    # u = user.get_user(request)
    u = User().GetUser(request)
    data = []
    if u != None:
        groups = Group().GetData()
        requested_group = [g['group_id'] for g in groups if g['group_code'] == body['group_code']]
        if len(requested_group) == 0:
            print('Invalid Group Code')
            data.append('Invalid Group Code')
        else:
            requested_group_id = requested_group[0]
            # print(requested_group_id)
            group_detail = Group_Detail().GetData()
            # reequest_group_detail = [g for g in group_detail if g['group_id'] == requested_group_id and g['email'] == u['email']]
            if len([g for g in group_detail if g['group_id'] == requested_group_id and g['email'] == u['email']]) > 0:
                data.append('User already part of Group')
            else:
                new_group_detail = {'group_detail_id' : Group_Detail().GetNextId(),
                                    'group_id': requested_group_id,
                                    'email': u['email'],
                                    'joined_on': datetime.now().strftime("%Y-%m-%d %H%M%S")

                }
                Group_Detail.AddData(new_group_detail)
                data.append('User added to the Group')
    return {'data': data}

def get_participating_polls(request: Request) -> dict:
    # u = user.get_user(request)
    u = User().GetUser(request)
    data = []
    if u != None:
        # For the given email, get the group_id from group_detail
        # For each group_id, get the poll_id from group
        # For each poll_id get poll data from poll
        group_detail = Group_Detail().GetData()
        group = Group().GetData()
        poll = Poll().GetData()
        data = [p for p in poll if p['poll_id'] in 
                    [g['poll_id'] for g in group if g['group_id'] in 
                        [gd['group_id'] for gd in group_detail if gd['email'] == u['email']]]
               ]
    return {'data': data}

def get_active_poll(request: Request) -> dict:
    # u = user.get_user(request)
    u = User().GetUser(request)
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
    # u = user.get_user(request)
    u = User().GetUser(request)
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