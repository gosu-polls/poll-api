
from fastapi import Request
from app.src.database.db.poll.group import Group as Group
from app.src.database.db.poll.group_detail import Group_Detail as Group_Detail
from app.src.database.db.poll.poll import Poll as Poll
from app.src.database.db.poll.point_config import Point_Config as Point_Config
from app.src.database.db.poll.user import User as User
from app.src.database.db.poll.super_user import Super_User as Super_User

from app.src.database.dbutil.poll_entity import Poll_Entity as Poll_Entity
from app.src.database.dbutil.poll_object import Poll_Object as Poll_Object

from app.src.database.db.vote.vote import Vote as Vote
from app.src.database.db.vote.vote_detail import Vote_Detail as Vote_Detail
from app.src.database.db.vote.ballot import Ballot as Ballot 

def get_super_user(request: Request) -> dict:
    u = User().GetUser(request)
    data = 0
    if u!= None:
        if Super_User().IsSuperUser(u):
            data = 1
        else:
            data = 0
    return {'data': data}

def reset_cache(request: Request) -> dict:
    u = User().GetUser(request)
    data = []
    if u != None:
        if Super_User().IsSuperUser(u):
            User().ResetCache()
            Group().ResetCache()
            Group_Detail().ResetCache()
            Point_Config().ResetCache()
            Poll().ResetCache()
            Super_User().ResetCache()

            polls = Poll().GetAvailablePolls(u)
            for p in polls:
                po = Poll_Object(Poll().GetPollObject(p['poll_id']))
                Ballot(po).ResetCache()
                Vote_Detail(po).ResetCache()
                Vote(po).ResetCache()

    return {'data': data}


def get_users(request: Request) -> dict:
    u = User().GetUser(request)
    data = []
    if u != None:
        if Super_User().IsSuperUser(u):
            data = User().GetData()
    return {'data': data}

def get_groups(request: Request) -> dict:
    u = User().GetUser(request)
    data = []
    if u != None:
        if Super_User().IsSuperUser(u):
            data = Group().GetData()
    return {'data': data}

def get_group_detail(request: Request) -> dict:
    u = User().GetUser(request)
    data = []
    if u != None:
        if Super_User().IsSuperUser(u):
            data = Group_Detail().GetData()
    return {'data': data}

def get_vote(request: Request, poll_id: int) -> dict:
    u = User().GetUser(request)
    data = []
    if u != None:
        if Super_User().IsSuperUser(u):
            po = Poll_Object(Poll().GetPollObject(poll_id))
            data = Vote(po).GetData()
    return {'data': data}

def get_vote_detail(request: Request, poll_id: int) -> dict:
    u = User().GetUser(request)
    data = []
    if u != None:
        if Super_User().IsSuperUser(u):
            po = Poll_Object(Poll().GetPollObject(poll_id))
            data = Vote_Detail(po).GetData()
    return {'data': data}

def get_ballot(request: Request, poll_id: int) -> dict:
    u = User().GetUser(request)
    data = []
    if u != None:
        if Super_User().IsSuperUser(u):
            po = Poll_Object(Poll().GetPollObject(poll_id))
            data = Ballot(po).GetData()
    return {'data': data}
