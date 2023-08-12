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
from datetime import datetime, timedelta

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
            # group_id = Group().GetNextId()
            new_group = {'group_name': body['group_name'],
                         'group_code': group_code,
                         'group_admin': u['email'],
                         'poll_id': body['available_poll']['poll_id']
                        }
            group_id = Group().AddData(new_group)
            # print(group_id)
            # print(group_id[0])
            # group_detail_id = Group_Detail().GetNextId()
            new_group_detail = {'group_id': group_id[0],
                                'email': u['email'],
                                'joined_on': datetime.utcnow().strftime("%Y-%m-%d %H%M%S")
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
                new_group_detail = {'group_id': requested_group_id,
                                    'email': u['email'],
                                    'joined_on': datetime.utcnow().strftime("%Y-%m-%d %H%M%S")
                }
                Group_Detail.AddData(new_group_detail)
                data.append('User added to the Group')
    return {'data': data}

def save_vote(request: Request, body: dict) -> dict:
    u = User().GetUser(request)
    data = []
    if u != None:
        # find the participating poll using poll id
        print(f'save_vote: The ballot for {u} is {body}')

        po = Poll_Object(Poll().GetPollObject(request, body['poll_id']))
        existing_ballot_vote = Ballot(po).GetUserVoteDetail(request, body['vote_id'])
        print(f'save_vote: Existing Ballot Vote is {existing_ballot_vote}')
        if len(existing_ballot_vote) == 0:
            new_ballot_vote = {
                'vote_id': body['vote_id'],
                'user_id': u['user_id'],
                'vote_detail_id': body['selected_vote_id'],
                'created_at': datetime.utcnow().strftime("%Y-%m-%d %H%M%S")
            }
            Ballot(po).AddData(new_ballot_vote)
        else:
            set_clause = {
                'vote_detail_id': body['selected_vote_id'],
                'updated_at': datetime.utcnow().strftime("%Y-%m-%d %H%M%S")
            }
            where_clause = {
                'ballot_id': existing_ballot_vote['ballot_id']
            }
            Ballot(po).UpdateData(set_clause, where_clause)
        # poll_id = Poll().GetDatum(body['poll_id'])
        
        # po = Poll_Object(poll_id)
        # ballot = Ballot(po).GetData()
    
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
        # print(f'get_active_poll: poll object of {pp} is {po.poll_name}.{po.poll_id}')
        vote = Vote(po).GetData()
        # print(f'get_active_poll all votes is {vote}')
        active_votes = [v for v in vote if ((datetime.utcnow() - timedelta(minutes = 10) if len(v['valid_from'].strip()) == 0 else datetime.strptime(v['valid_from'], '%Y-%m-%d %H%M%S'))
                                            <= datetime.utcnow() <= 
                                            (datetime.utcnow() + timedelta(minutes = 10) if len(v['valid_to'].strip()) == 0 else datetime.strptime(v['valid_to'], '%Y-%m-%d %H%M%S')))
                       ]
        # print(f'get_active_poll active_votes is {active_votes}')
        vote_detail = Vote_Detail(po).GetData()
        # ballot = Ballot(po).GetUserBallot(request)
        
        # print("get_active_poll: vote: ", vote)
        # print(vote_detail)
        # for each poll_id, get the vote
        # for each vote, get vote_detail
        # for each vote_detail get ballot
        poll_data = []
        for v in active_votes:
            ballot = Ballot(po).GetUserVoteDetail(request, v['vote_id'])
            # print(f'get_active_poll: ballot for vote {v} is {ballot}')
            # v['selected_vote_detail_id'] = -1 # this is just a hack
            v['selected_vote_detail_id'] = ballot['vote_detail_id'] if 'vote_detail_id' in ballot else -1
            vd = [vd for vd in vote_detail if vd['vote_id'] == v['vote_id']]
            v['vote_detail'] = vd 
            # print('get_active_poll: v: ', v)
            poll_data.append(v)
            
            # poll_data = [vd for vd in vote_detail if vd['vote_id'] in 
            #                 [v['vote_id'] for v in vote]
            #             ]
        data.append({'poll_id': pp['poll_id'],
                    #  'vote_title': v['vote_title'],
                        'data': poll_data})
        # data.append({pp['poll_id']: poll_data})
    
    print(f'get_active_poll: Participating Polls data is {data}')
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