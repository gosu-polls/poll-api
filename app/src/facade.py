# import functools
import json
import jwt
from fastapi import Request

from src.database.db.poll.group import Group as Group
from src.database.db.poll.group_detail import Group_Detail as Group_Detail
from src.database.db.poll.poll import Poll as Poll
from src.database.db.poll.point_config import Point_Config as Point_Config
from src.database.db.poll.user import User as User

from src.database.dbutil.poll_object import Poll_Object as Poll_Object

from src.database.db.vote.vote import Vote as Vote
from src.database.db.vote.vote_detail import Vote_Detail as Vote_Detail
from src.database.db.vote.ballot import Ballot as Ballot 

import uuid
from datetime import datetime, timedelta
import pandas as pd


def get_available_polls(request: Request) -> dict:
    u = User().GetUser(request)
    data = []
    if u != None:
        data = Poll().GetAvailablePolls(u)
    return {'data': data}

def get_my_groups(request: Request) -> dict:
    u = User().GetUser(request)
    data = []
    if u != None:
        data = Group().GetAdminGroups(u)
    # data = Group().GetAdminGroups(request)
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
                         'group_admin_user_id': u['user_id'],
                         'group_admin': u['email'],
                         'poll_id': body['available_poll']['poll_id']
                        }
            group_id = Group().AddData(new_group)
            # print(group_id)
            # print(group_id[0])
            # group_detail_id = Group_Detail().GetNextId()
            new_group_detail = {'group_id': group_id[0],
                                'user_id': u['user_id'],
                                'email': u['email'],
                                'joined_on': datetime.utcnow().strftime("%Y-%m-%d %H%M%S")
                                }
            Group_Detail().AddData(new_group_detail)
            # data = _get_my_groups(request)
            data = Group().GetAdminGroups(u)
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
            if len([g for g in group_detail if g['group_id'] == requested_group_id and g['user_id'] == u['user_id']]) > 0:
                data.append('User already part of Group')
            else:
                new_group_detail = {'group_id': requested_group_id,
                                    'user_id': u['user_id'],
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
        # print(f'save_vote: The ballot for {u} is {body}')

        po = Poll_Object(Poll().GetPollObject(body['poll_id']))
        # print(f'save_vote : po is {po}')
        if Vote(po).IsVoteActive(body['vote_id']):
            existing_ballot_vote = Ballot(po).GetUserVoteDetail(u, body['vote_id'])
            # print(f'save_vote: Existing Ballot Vote is {existing_ballot_vote}')
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
                Ballot(po).UpdateData(set_clause=set_clause, where_clause=where_clause)

            # poll_id = Poll().GetDatum(body['poll_id'])
            
            # po = Poll_Object(poll_id)
            # ballot = Ballot(po).GetData()
        else:
            print('Cannot Vote anymore. It is frozen')

    return {'data': data}

def get_participating_polls(request: Request) -> dict:
    u = User().GetUser(request)
    data = []
    # print(f'get_participating_polls -> u {u}')
    if u != None:
        data = Poll().GetParticipatingPolls(u)
    # data = Poll().GetParticipatingPolls(request)
    return {'data': data}

def get_vote_section(request: Request) -> dict:
    data = []
    u = User().GetUser(request)
    if u != None:
        data = get_active_poll(u)
    return {'data': data}

def get_active_poll(u : User) -> dict:
    data = []
    participating_polls = Poll().GetParticipatingPolls(u)

    for pp in participating_polls:
        po = Poll_Object(pp)
        # print(f'get_active_poll: poll object of {pp} is {po.poll_name}.{po.poll_id}')
        vote = Vote(po).GetData()
        # print(f'get_active_poll all votes is {vote}')
        active_votes = [v for v in vote if (((datetime.utcnow() - timedelta(minutes = 10) if len(v['valid_from'].strip()) == 0 else datetime.strptime(v['valid_from'], '%Y-%m-%d %H%M%S'))
                                            <= datetime.utcnow() <= 
                                            (datetime.utcnow() + timedelta(minutes = 10) if len(v['valid_to'].strip()) == 0 else datetime.strptime(v['valid_to'], '%Y-%m-%d %H%M%S')))) 
                                            # and (Vote(po).IsVoteActive(request, v['vote_id']))
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
            ballot = Ballot(po).GetUserVoteDetail(u, v['vote_id'])
            # print(f'get_active_poll: ballot for vote {v} is {ballot}')
            # v['selected_vote_detail_id'] = -1 # this is just a hack
            v['selected_vote_detail_id'] = ballot['vote_detail_id'] if 'vote_detail_id' in ballot else -1
            # v['submitted_right_answer'] = vote_detail
            vd = [vd for vd in vote_detail if vd['vote_id'] == v['vote_id']]
            v['vote_detail'] = vd
            # print('get_active_poll: v: ', v)
            poll_data.append(v)
        data.append({'poll_id': pp['poll_id'],
                     'is_admin': 'Y' if pp['admin_user_id'] == u['user_id'] else 'N',
                     'data': poll_data})
        # data.append({pp['poll_id']: poll_data})
    
    # print(f'get_active_poll: Participating Polls data is {data}')
    # pprint.PrettyPrinter(width=20).pprint(f'get_active_poll: Participating Polls data is {data}')
    return data

def get_poll_history_v2(request: Request) -> dict:
    data = []
    u = User().GetUser(request)
    if u != None:
        data = [{'poll_id' : 1,
            'vote_detail' : [{'vote_id' : 1,
                            'vote_title' : 'Eng vs Nz',
                            'vote_option' : [{'option': 'Eng',
                                                'user_data' : [{'name': 'Kiran Gosu', 'initial': 'KG', 'picture': 'https://lh3.googleusercontent.com/a/AAcHTtebPZq-IT9DjR2sQJP5Yl2ziMSbqR01tawoINV4HFNu2paO=s96-c'}]
                                            },
                                            {'option': 'Nz',
                                                'user_data' : [{'name': 'Arunmozhidevan G', 'initial': 'AG', 'picture': 'https://lh3.googleusercontent.com/a/AAcHTtebPZq-IT9DjR2sQJP5Yl2ziMSbqR01tawoINV4HFNu2paO=s96-c'}]
                                            },
                                            {'option': 'NR/Tie',
                                                'user_data' : [{'name': 'Sivapragasam Muthu', 'initial': 'SM', 'picture': 'https://lh3.googleusercontent.com/a/AAcHTtebPZq-IT9DjR2sQJP5Yl2ziMSbqR01tawoINV4HFNu2paO=s96-c'},
                                                            {'name': 'Kailash Kadhiresan', 'initial': 'KK', 'picture': 'https://lh3.googleusercontent.com/a/AAcHTtebPZq-IT9DjR2sQJP5Yl2ziMSbqR01tawoINV4HFNu2paO=s96-c'}
                                                            ]
                                            }
                                            ]
                            },
                            {'vote_id' : 2,
                            'vote_title' : 'Ned vs Pak',
                            'vote_option' : [{'option': 'Ned',
                                                'user_data' : [{'name': 'Kiran Gosu', 'initial': 'KG', 'picture': 'https://lh3.googleusercontent.com/a/AAcHTtebPZq-IT9DjR2sQJP5Yl2ziMSbqR01tawoINV4HFNu2paO=s96-c'},
                                                            {'name': 'Sivapragasam Muthu', 'initial': 'SM', 'picture': 'https://lh3.googleusercontent.com/a/AAcHTtebPZq-IT9DjR2sQJP5Yl2ziMSbqR01tawoINV4HFNu2paO=s96-c'}
                                                            ]
                                            },
                                            {'option': 'Pak',
                                                'user_data' : [{'name': 'Arunmozhidevan G', 'initial': 'AG', 'picture': 'https://lh3.googleusercontent.com/a/AAcHTtebPZq-IT9DjR2sQJP5Yl2ziMSbqR01tawoINV4HFNu2paO=s96-c'},
                                                            {'name': 'Kailash Kadhiresan', 'initial': 'KK', 'picture': 'https://lh3.googleusercontent.com/a/AAcHTtebPZq-IT9DjR2sQJP5Yl2ziMSbqR01tawoINV4HFNu2paO=s96-c'}
                                                            ]
                                            },
                                            {'option': 'NR/Tie',
                                                'user_data' : []
                                            }
                                            ]
                            }
                            ]
        },
        {'poll_id' : 2,
            'vote_detail' : [{'vote_id' : 1,
                            'vote_title' : 'Bra vs Arg',
                            'vote_option' : [{'option': 'Bra',
                                                'user_data' : [{'name': 'Arunmozhidevan G', 'initial': 'AG', 'picture': 'https://lh3.googleusercontent.com/a/AAcHTtebPZq-IT9DjR2sQJP5Yl2ziMSbqR01tawoINV4HFNu2paO=s96-c'}]
                                            },
                                            {'option': 'Nz',
                                                'user_data' : []
                                            },
                                            {'option': 'NR/Tie',
                                                'user_data' : [{'name': 'Kiran Gosu', 'initial': 'KG', 'picture': 'https://lh3.googleusercontent.com/a/AAcHTtebPZq-IT9DjR2sQJP5Yl2ziMSbqR01tawoINV4HFNu2paO=s96-c'}]
                                            }
                                            ]
                            }
                            ]
        }
        ]
    return {'data': data}


def get_poll_history(request: Request) -> dict:
    data = []
    u = User().GetUser(request)
    if u != None:

        # participating_polls = Poll().GetParticipatingPolls(request)
        # for pp in participating_polls:
        #     po = Poll_Object(pp)
        #     vote = Vote(po).GetData()
        #     vote_detail = Vote_Detail(po).GetData()
        #     ballot = Ballot(po).GetData()
            # for each participating poll (cwc/fifa)
            # for each vote underneath
        


    # u = User().GetUser(request)
    # if u != None:
        [
          {'poll_id': 1, 
           'data': [{'vote_id': 1, 
                     'vote_title': 'Eng vs Nz', 
                     'valid_from': '', 
                     'valid_to': '2023-10-05 090000', 
                     'poll_id': 1, 
                     'selected_vote_detail_id': 2, 
                     'vote_detail': [{'vote_detail_id': 1, 'vote_id': 1, 'option': 'Eng'}, 
                                     {'vote_detail_id': 2, 'vote_id': 1, 'option': 'NZ'}, 
                                     {'vote_detail_id': 3, 'vote_id': 1, 'option': 'NR/Tie'}
                                    ]
                    }
                   ]
          }, 
          {'poll_id': 2, 
           'data': [{'vote_id': 1, 
                     'vote_title': 'Bra vs Arg', 
                     'valid_from': '', 
                     'valid_to': '2023-10-05 090000', 
                     'poll_id': 2, 
                     'selected_vote_detail_id': 1, 
                     'vote_detail': [{'vote_detail_id': 1, 'vote_id': 1, 'option': 'Bra'}, 
                                     {'vote_detail_id': 2, 'vote_id': 1, 'option': 'Arg'}, 
                                     {'vote_detail_id': 3, 'vote_id': 1, 'option': 'NR/Tie'}
                                    ]
                    }
                   ]
          }
        ]
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
    
    return {'data': data}

def freeze_vote(request: Request, body: dict) -> dict:
    u = User().GetUser(request)
    data = []
    if u != None:
        if Poll().IsUserAdmin(u, body['poll_id']):
            # print(body)
            po = Poll_Object(Poll().GetPollObject(body['poll_id']))
            set_clause = {'is_open': 'N' if body['is_open'] == 'Y' else 'Y'}
            where_clause = {'vote_id': body['vote_id']}
            Vote(po).UpdateData(set_clause=set_clause, where_clause=where_clause)
            data = get_active_poll(u)
    return {'data': data}

def submit_answer(request: Request, body: dict) -> dict:
    u = User().GetUser(request)
    data = []
    # print(f'submit_answer body from UI is: {body}')
    # print(body)
    if u != None:
        if Poll().IsUserAdmin(u, body['poll_id']):
            po = Poll_Object(Poll().GetPollObject(body['poll_id']))
            vote_detail_data = body['vote_detail']
            vote_detail_data_df = pd.DataFrame(vote_detail_data)
            vote_detail_data_df['updated_at'] = datetime.utcnow().strftime("%Y-%m-%d %H%M%S")
            Vote_Detail(po).UpdateData(block_data_df=vote_detail_data_df)
            
        data = get_active_poll(u)
    return {'data': data}


def calc_points(request: Request, body: dict) -> dict:
    u = User().GetUser(request)
    data = []
    if u != None:
        if Poll().IsUserAdmin(u, body['poll_id']):
            point_config_data = Point_Config().GetPointsConfigForPoll(poll_id=body['poll_id'])

            po = Poll_Object(Poll().GetPollObject(body['poll_id']))
            ballot = Ballot(po).GetData()
            vote_detail = Vote_Detail(po).GetData()
            vote = Vote(po).GetData()
            ballot_data = [dict(b, points = point_config_data['right'] if vd['is_right'] == 'Y' else point_config_data['wrong'] ) for b in ballot for
                            vd in vote_detail if vd['vote_id'] in 
                                [v['vote_id'] for v in vote if v['is_open'] == 'N']
                                    if b['vote_detail_id'] == vd['vote_detail_id']            
                          ]
            ballot_data_df = pd.DataFrame(ballot_data)
            ballot_data_df['updated_at'] = datetime.utcnow().strftime("%Y-%m-%d %H%M%S")
            Ballot(po).UpdateData(block_data_df=ballot_data_df)
    return {'data': data}

def get_group_points(request: Request, body: dict) -> dict:
    u = User().GetUser(request)
    data = []
    if u != None:
        # Find all the groups the user is associated with under this poll.
        # Get group wise split for this poll
        # Assume the user is part of two group viz., office, friends.
        # The output must be like this:
        [
            {
                'group_name': 'office',
                'points_data': [
                                    {'user': {'name': 'Kiran Gosu', 'Initials' : 'KG', 'Picture': 'url'},
                                    'consolidated_points': 1,
                                    'split': [{
                                                    'ENG vs NZ': -1,
                                                    'NED vs PAK': 2,
                                                    'AFG vs BAN': 0
                                                }]
                                    },
                                    {'user': {'name': 'Anand', 'Initials' : 'AJ', 'Picture': 'url'},
                                    'consolidated_points': 3,
                                    'split': [{
                                                    'ENG vs NZ': 2,
                                                    'NED vs PAK': 2,
                                                    'AFG vs BAN': -1
                                                }]
                                    },
                                    {'user': {'name': 'Praveen', 'Initials' : 'PS', 'Picture': 'url'},
                                    'consolidated_points': 0,
                                    'split': [{
                                                    'ENG vs NZ': 2,
                                                    'NED vs PAK': -1,
                                                    'AFG vs BAN': -1
                                                }]
                                    }
                ]
            },

            {
                'group_name': 'friends',
                'points_data': [
                                    {'user': {'name': 'Kiran Gosu', 'Initials' : 'KG', 'Picture': 'url'},
                                    'consolidated_points': 1,
                                    'split': [{
                                                    'ENG vs NZ': -1,
                                                    'NED vs PAK': 2,
                                                    'AFG vs BAN': 0
                                                }]
                                    },
                                    {'user': {'name': 'Sivapragasam Muthu', 'Initials' : 'SM', 'Picture': 'url'},
                                    'consolidated_points': 6,
                                    'split': [{
                                                    'ENG vs NZ': 2,
                                                    'NED vs PAK': 2,
                                                    'AFG vs BAN': 2
                                                }]
                                    },
                                    {'user': {'name': 'Arunmozhidevan G', 'Initials' : 'AG', 'Picture': 'url'},
                                    'consolidated_points': 3,
                                    'split': [{
                                                    'ENG vs NZ': 2,
                                                    'NED vs PAK': 2,
                                                    'AFG vs BAN': -1
                                                }]
                                    }
                ]
            }
        ]
        pass
    return {'data': data}