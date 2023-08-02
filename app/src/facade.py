# import functools
import json
import jwt
from fastapi import Request

from src.database.db.poll.group import Group as Group
from src.database.db.poll.group_detail import Group_Detail as Group_Detail
from src.database.db.poll.poll import Poll as Poll
from src.database.db.poll.user import User as User

from src.database.dbutil.poll_object import Poll_Object as Poll_Object

from src.database.db.vote.vote import Vote as Vote
from src.database.db.vote.vote_detail import Vote_Detail as Vote_Detail
from src.database.db.vote.ballot import Ballot as Ballot 

import uuid
from datetime import datetime

# class polls():
#     def init():
#         pass

# def login_required(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         request = args[0]
#         header = ''
#         header = json.loads(request.headers.get('Token'))
#         if header == None:
#             return func(*args, **kwargs)
#         else:
#             return func(*args, **kwargs)
#     return wrapper

# Private Methods
# def _get_my_groups(request: Request) -> list:
#     u = User().GetUser(request)
#     data = []
#     if u != None:
#         groups = Group().GetData()
#         header = json.loads(request.headers.get('Token'))
#         if header != None:
#             email = jwt.decode(header['jwt'], 'secret', 'HS256')['email']
#             data = [g for g in groups if g['group_admin'] == email]

#     return data

def get_available_polls(request: Request) -> dict:
    data = Poll().GetAvailablePolls(request)
    # u = User().GetUser(request)
    # data = []
    # if u != None:
    #     data = Poll().GetData()
    return {'data': data}

def get_groups_admin(request: Request) -> dict:
    # u = User().GetUser(request)
    # data = []
    # if u != None:
    #     data = _get_my_groups(request)
    data = Group().GetAdminGroups(request)
    return {'data': data}

def create_group(request: Request, body: dict) -> dict:
    u = User().GetUser(request)
    data = []
    if u != None:
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
            new_group_detail = {'group_detail_id' : group_detail_id,
                                'group_id': group_id,
                                'email': u['email'],
                                'joined_on': datetime.now().strftime("%Y-%m-%d %H%M%S")
                                }
            Group_Detail().AddData(new_group_detail)
            # data = _get_my_groups(request)
            data = Group().GetAdminGroups(request)
            # data.append('Group Created')
            
    return {'data': data}

def join_group(request: Request, body: dict) -> dict:
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
            group_detail = Group_Detail().GetData()
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

def save_vote(request: Request, body: dict) -> dict:
    u = User().GetUser(request)
    data = []
    if u != None:
        # find the participating poll using poll id
        poll = Poll().GetDatum(body['poll_id'])
        po = Poll_Object(poll)
        ballot = Ballot(po).GetData()
    
    return {'data': data}

def get_participating_polls(request: Request) -> dict:
    # u = User().GetUser(request)
    # data = []
    # if u != None:
    #     data = Poll().GetParticipatingPolls(u['email'])
    data = Poll().GetParticipatingPolls(request)
    return {'data': data}

def get_active_poll(request: Request) -> dict:
    data = []
    # u = User().GetUser(request)
    # if u != None:
    participating_polls = Poll().GetParticipatingPolls(request)
    # print(f'Participating Polls are {participating_polls}')

    for pp in participating_polls:
        po = Poll_Object(pp)
        # print(f'poll object of {pp} is {po.poll_name}.{po.poll_id}')
        vote = Vote(po).GetData()
        vote_detail = Vote_Detail(po).GetData()
        print(vote)
        print(vote_detail)
        # for each poll_id, get the vote
        # for each vote, get vote_detail
        # for each vote_detail get ballot
        poll_data = []
        for v in vote:
            vd = [vd for vd in vote_detail if vd['vote_id'] == v['vote_id']]
            v['vote_detail'] = vd 
            poll_data.append(v)
            
            # poll_data = [vd for vd in vote_detail if vd['vote_id'] in 
            #                 [v['vote_id'] for v in vote]
            #             ]
        data.append({'poll_id': pp['poll_id'],
                    #  'vote_title': v['vote_title'],
                        'data': poll_data})
        # data.append({pp['poll_id']: poll_data})
    
    print(f'Participating Polls data is {data}')
    return {'data': data}
    
def get_poll_history(request: Request) -> dict:
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