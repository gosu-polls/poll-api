from fastapi import FastAPI, Request
from requests import request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import urllib.request
import app.src.auth.auth as auth
import app.src.facade as facade
import app.src.sudo as sudo
from app.src.database.db.test.match import Match as Match
from app.src.database.db.test.country import Country as Country
from app.src.database.db.poll.group import Group as Group
from app.src.database.db.poll.poll import Poll as Poll
from app.src.database.db.poll.point_config import Point_Config as Point_Config
from datetime import datetime
# from app.src.database.db.test.cosmos.country_v2 import Country as Country_v2
# from app.src.database.db.test.cosmos.user import User as User

from app.test.t_polls import TestSuite as TestSuite
import pandas as pd
# import functools
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
origins = [
    # "http://localhost",
    # "http://localhost:8080",
    # "http://localhost:8000",
    # "http://localhost:8001",
    "http://localhost:3000",
    # "http://localhost:3001",
    "https://polls-by-gosu.azurewebsites.net",
    "https://polls-by-gosu.azurewebsites.net/login",
    "https://polls-by-gosu.azurewebsites.net/*",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# add_middleware(
#     TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"]
# )
@app.get("/")
def read_root():
    try:
        
        urllib.request.urlopen("https://www.Tutorialspoint.com")
        return {"Polls": f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} The Internet is connected."}
    except urllib.error.URLError:
        return {"Polls": f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} The Internet is not connected."}


# def login_required(func):
#     @functools.wraps(func)
#     async def wrapper(*args, **kwargs):
#         header = json.loads(kwargs['request'].headers.get('Token'))
#         if header == None:
#             print('None')
#             # return None
#             return await None
#         else:
#             print(jwt.decode(header['jwt'], 'secret', 'HS256')['email'])
#             return await func(*args, **kwargs)
#     return wrapper

# def login_required(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         header = json.loads(kwargs['request'].headers.get('Token'))
#         if header == None:
#             print('None')
#             # return None
#             # return func(*args, **kwargs)
#         else:
#             print(jwt.decode(header['jwt'], 'secret', 'HS256')['email'])
#             return func(*args, **kwargs)
#     return wrapper

# @app.get("/poll")
# @login_required
# def get_active_poll(request : Request) -> dict:
#     my_header = request.headers.get('Token')
#     header = json.loads(my_header)
#     return app.src.polls.get_active_poll()

# @app.get("/users")
# def get_users() -> dict:
#     try:
#         data = User().GetUsers()
#         return {"data": data}
#     except Exception as err:
#         return {"exception": err}

# Cosmos DB
# @app.get("/countries_v2")
# def get_countries_v2() -> dict:
#     try:
#         data = Country_v2().GetCountries()
#         return {"data": data}
#     except Exception as err:
#         return {"exception": err}


# Test API (does not need authentication)
@app.get("/matches")
def get_matches() -> dict:
    try:
        data = Match().GetData()
        return {"data": data}
    except Exception as err:
        return {"exception": str(err)}
    
@app.get("/matches/{id}")
def get_match(id : int) -> dict:
    try:
        data = Match().GetDatum(id)
        return {"data": data}
    except Exception as err:
        return {"exception": str(err)}
        
@app.get("/countries")
def get_countries() -> dict:
    try:
        data = Country().GetData()
        return {"data": data}
    except Exception as err:
        return {"exception": str(err)}
    
@app.get("/countries/{id}")
def get_match(id : int) -> dict:
    try:
        data = Country().GetDatum(id)
        return {"data": data}
    except Exception as err:
        return {"exception": err}


# Actual Application API end points
# Requires Facade
@app.post("/login")
def login(request: dict) -> dict:
    response = auth.handle_user(request)
    return {"data" : response}

@app.get("/availablepolls")
def get_available_polls(request: Request) -> dict:
    data = facade.get_available_polls(request)
    return data

@app.post("/creategroup")
def create_group(request: Request, body: dict) -> dict:
    data = facade.create_group(request, body)
    return data

@app.post("/joingroup")
def join_group(request: Request, body: dict) -> dict:
    data = facade.join_group(request, body)
    return data

@app.get("/mygroups")
def get_my_groups(request: Request) -> dict:
    data = facade.get_my_groups(request)
    return data

@app.get("/participatingpolls")
def get_participating_polls(request: Request) -> dict:
    data = facade.get_participating_polls(request)
    return data

@app.get("/votesection")
def get_active_poll(request: Request) -> dict:
    data = facade.get_vote_section(request)
    return data

@app.post("/savevote")
def save_vote(request: Request, body: dict) -> dict:
    data = facade.save_vote(request, body)
    return data

@app.get("/pollhistory")
def get_poll_history(request: Request) -> dict:
    data = facade.get_poll_history(request)
    return data

@app.post("/freezevote")
def freeze_vote(request: Request, body: dict) -> dict:
    data = facade.freeze_vote(request, body)
    return data

@app.put("/submitanswer")
def submit_answer(request: Request, body: dict) -> dict:
    data = facade.submit_answer(request, body)
    return data

@app.put("/calcpoints")
def calc_points(request: Request, body: dict):
    data = facade.calc_points(request, body)
    return data

@app.get("/grouppoints")
def get_group_points(request: Request) -> dict:
    data = facade.get_group_points(request)
    return data

@app.get("/superuser")
def get_super_user(request: Request) -> dict:
    data = sudo.get_super_user(request)
    return data

@app.put("/suresetcache")
def reset_cache(request: Request) -> dict:
    data = sudo.reset_cache(request)
    return data

@app.get("/sugetusers")
def get_su_users(request: Request) -> dict:
    data = sudo.get_users(request)
    return data

@app.get("/sugetgroups")
def get_su_groups(request: Request) -> dict:
    data = sudo.get_groups(request)
    return data

@app.get("/sugetgroupdetail")
def get_su_group_detail(request: Request) -> dict:
    data = sudo.get_group_detail(request)
    return data

@app.get("/sugetvote/{poll_id}")
def get_su_vote(request: Request, poll_id: int) -> dict:
    data = sudo.get_vote(request, poll_id)
    return data

@app.get("/sugetvotedetail/{poll_id}")
def get_su_vote_detail(request: Request, poll_id: int) -> dict:
    data = sudo.get_vote_detail(request, poll_id)
    return data

@app.get("/sugetballot/{poll_id}")
def get_su_ballot(request: Request, poll_id: int) -> dict:
    data = sudo.get_ballot(request, poll_id)
    return data


def run_tests():
    # TestSuite().test_get_poll(1)
    # TestSuite().test_vote_detail()
    logged_user_id = 1
    groups = [ {'group_id' : 1, 'group_name': 'apple', 'admin_user_id': 1},
               {'group_id' : 2, 'group_name': 'android', 'admin_user_id': 2}
            ]
    
    # data = [g for g in groups]
    # data = [dict(g, is_admin= 'Y' if g['admin_user_id'] == logged_user_id else 'N' ) for g in groups]

    # print(data)
    votes = {
        'vote_id' : [1, 2, 3, 4, 5],
        'vote_title' : ['ENG vs NZ', 'NED vs PAK', 'AFG vs BAN', 'RSA vs SRI', 'IND vs AUS'],
        'is_open': ['N', 'Y', '', '', '']
    }
    df = pd.DataFrame(votes)
    filter = {'is_open': 'N'}
    k = list(filter.keys())[0]
    v = filter[k]
    # print(k, v)
    # print(df)
    # print(df.loc[df[k] == v])

    # User:     vote_id         is_right    vote_id             is_right    points
    # 1 - KG    1 - Eng vs NZ   Y           2 - NED vs PAK      N           2 - 1 = 1
    # 2 - SM    1 - Eng vs Nz   Y           2 - NED vs PAK      Y           2 + 2 = 4
    # 3 - AG    1 - Eng vs Nz   N           2 - NED vs PAK      Y          -1 + 2 = 1 
    # 4 - KK                                2 - NED vs PAK      Y           0 + 2 = 2
    # 5 - AR    1 - Eng vs Nz   N                                          -1 + 0 = -1

    point_config = {'right': 2, 'wrong': -2}
    poll_id = 3
    point_config_id = Poll().GetDatum(poll_id)['point_config_id']
    print(point_config_id)
    if '{}'.format(point_config_id).isdigit():
        print('if')
        point_config = Point_Config().GetDatum(point_config_id)
        print(f'if {point_config}')
    else:
        print('else')
        point_config_data = Point_Config().GetFilteredData({'point_config_name' : 'default'})
        print(f'else {point_config_data}')
        if len(point_config_data) > 0:
            point_config = point_config_data[0]
    
    # print(point_config_data)
    # if len(point_config_data) > 0:
    #     point_config = point_config_data[0]
    # else:
    #     point_config = {'right': 2, 'wrong': 0}        
    
    print(point_config)
    ballot = [ {'ballot_id': -1, 'vote_id': -1, 'user_id': -1, 'vote_detail_id': -1, 'points': ''},
               
               {'ballot_id': 0,  'vote_id': 1,  'user_id': 1,  'vote_detail_id': 2,  'points': ''},
               {'ballot_id': 1,  'vote_id': 1,  'user_id': 2,  'vote_detail_id': 2,  'points': ''},
               {'ballot_id': 2,  'vote_id': 1,  'user_id': 3,  'vote_detail_id': 1,  'points': ''},
               {'ballot_id': 3,  'vote_id': 1,  'user_id': 5,  'vote_detail_id': 3,  'points': ''},

               {'ballot_id': 4,  'vote_id': 2,  'user_id': 1,  'vote_detail_id': 4,  'points': ''},
               {'ballot_id': 5,  'vote_id': 2,  'user_id': 2,  'vote_detail_id': 6,  'points': ''},
               {'ballot_id': 6,  'vote_id': 2,  'user_id': 3,  'vote_detail_id': 6,  'points': ''},
               {'ballot_id': 7,  'vote_id': 2,  'user_id': 4,  'vote_detail_id': 6,  'points': ''},
             ]
    vote_detail = [ {'vote_detail_id': 1, 'vote_id': 1, 'option': 'Eng', 'is_right': 'N'},
                    {'vote_detail_id': 2, 'vote_id': 1, 'option': 'Nz', 'is_right': 'Y'},
                    {'vote_detail_id': 3, 'vote_id': 1, 'option': 'NR/Tie', 'is_right': 'N'},
                    {'vote_detail_id': 4, 'vote_id': 2, 'option': 'Ned', 'is_right': 'N'},
                    {'vote_detail_id': 5, 'vote_id': 2, 'option': 'Pak', 'is_right': 'N'},
                    {'vote_detail_id': 6, 'vote_id': 2, 'option': 'NR/Tie', 'is_right': 'Y'}
                  ]	

    vote = [ {'vote_id': 1, 'vote_title': 'ENG vs NZ', 'valid_from': '', 'valid_to': '2023-10-05 080000', 'is_open': 'N'},
             {'vote_id': 2, 'vote_title': 'NED vs PAK', 'valid_from': '', 'valid_to': '2023-10-06 080000', 'is_open': 'N'},
             {'vote_id': 3, 'vote_title': 'AFG vs BAN', 'valid_from': '2023-10-06 043000', 'valid_to': '2023-10-07 043000', 'is_open': ''},
             {'vote_id': 4, 'vote_title': 'RSA vs SRI', 'valid_from': '2023-10-06 080000', 'valid_to': '2023-10-07 080000', 'is_open': ''},
             {'vote_id': 5, 'vote_title': 'IND vs AUS', 'valid_from': '2023-10-07 080000', 'valid_to': '2023-10-08 080000', 'is_open': ''}
           ]

    # print([[dict(b, points=2 if vd['is_right'] == 'Y' else -1 ), vd] for b in ballot for
    #         vd in vote_detail if vd['vote_id'] in 
    #             [v['vote_id'] for v in vote if v['is_open'] == 'N']
    #         if b['vote_detail_id'] == vd['vote_detail_id']
            
    #       ]
    #      )


    print([dict(b, points = point_config['right'] if vd['is_right'] == 'Y' else point_config['wrong'] ) for b in ballot for
            vd in vote_detail if vd['vote_id'] in 
                [v['vote_id'] for v in vote if v['is_open'] == 'N']
            if b['vote_detail_id'] == vd['vote_detail_id']
            
          ]
         )
    
    [
        {'ballot_id': 0, 'vote_id': 1, 'user_id': 1, 'vote_detail_id': 2, 'points': 2}, 
        {'ballot_id': 1, 'vote_id': 1, 'user_id': 2, 'vote_detail_id': 2, 'points': 2}, 
        {'ballot_id': 2, 'vote_id': 1, 'user_id': 3, 'vote_detail_id': 1, 'points': -1}, 
        {'ballot_id': 3, 'vote_id': 1, 'user_id': 5, 'vote_detail_id': 3, 'points': -1}, 
        {'ballot_id': 4, 'vote_id': 2, 'user_id': 1, 'vote_detail_id': 4, 'points': -1}, 
        {'ballot_id': 5, 'vote_id': 2, 'user_id': 2, 'vote_detail_id': 6, 'points': 2}, 
        {'ballot_id': 6, 'vote_id': 2, 'user_id': 3, 'vote_detail_id': 6, 'points': 2}, 
        {'ballot_id': 7, 'vote_id': 2, 'user_id': 4, 'vote_detail_id': 6, 'points': 2}]

    [
        [{'ballot_id': 0, 'vote_id': 1, 'user_id': 1, 'vote_detail_id': 2, 'points': 2}, 
         {'vote_detail_id': 2, 'vote_id': 1, 'option': 'Nz', 'is_right': 'Y'}], 
        [{'ballot_id': 1, 'vote_id': 1, 'user_id': 2, 'vote_detail_id': 2, 'points': 2}, 
         {'vote_detail_id': 2, 'vote_id': 1, 'option': 'Nz', 'is_right': 'Y'}], 
        [{'ballot_id': 2, 'vote_id': 1, 'user_id': 3, 'vote_detail_id': 1, 'points': -1}, 
         {'vote_detail_id': 1, 'vote_id': 1, 'option': 'Eng', 'is_right': 'N'}], 
        [{'ballot_id': 3, 'vote_id': 1, 'user_id': 5, 'vote_detail_id': 3, 'points': -1}, 
         {'vote_detail_id': 3, 'vote_id': 1, 'option': 'NR/Tie', 'is_right': 'N'}], 
        [{'ballot_id': 4, 'vote_id': 2, 'user_id': 1, 'vote_detail_id': 4, 'points': -1}, 
         {'vote_detail_id': 4, 'vote_id': 2, 'option': 'Ned', 'is_right': 'N'}], 
        [{'ballot_id': 5, 'vote_id': 2, 'user_id': 2, 'vote_detail_id': 6, 'points': 2}, 
         {'vote_detail_id': 6, 'vote_id': 2, 'option': 'NR/Tie', 'is_right': 'Y'}], 
        [{'ballot_id': 6, 'vote_id': 2, 'user_id': 3, 'vote_detail_id': 6, 'points': 2}, 
         {'vote_detail_id': 6, 'vote_id': 2, 'option': 'NR/Tie', 'is_right': 'Y'}], 
        [{'ballot_id': 7, 'vote_id': 2, 'user_id': 4, 'vote_detail_id': 6, 'points': 2}, 
         {'vote_detail_id': 6, 'vote_id': 2, 'option': 'NR/Tie', 'is_right': 'Y'}]
    ]

    # [{'ballot_id': -1, 'vote_id': -1, 'user_id': -1, 'vote_detail_id': -1, 'points': ''}, 
    #  {'ballot_id': -1, 'vote_id': -1, 'user_id': -1, 'vote_detail_id': -1, 'points': ''}, 
    #  {'ballot_id': -1, 'vote_id': -1, 'user_id': -1, 'vote_detail_id': -1, 'points': ''}, 
    #  {'ballot_id': -1, 'vote_id': -1, 'user_id': -1, 'vote_detail_id': -1, 'points': ''}, 
    #  {'ballot_id': -1, 'vote_id': -1, 'user_id': -1, 'vote_detail_id': -1, 'points': ''}, 
    #  {'ballot_id': -1, 'vote_id': -1, 'user_id': -1, 'vote_detail_id': -1, 'points': ''}, 
    #  {'ballot_id': 0, 'vote_id': 1, 'user_id': 1, 'vote_detail_id': 1, 'points': ''}, 
    #  {'ballot_id': 0, 'vote_id': 1, 'user_id': 1, 'vote_detail_id': 1, 'points': ''}, {'ballot_id': 0, 'vote_id': 1, 'user_id': 1, 'vote_detail_id': 1, 'points': ''}, {'ballot_id': 0, 'vote_id': 1, 'user_id': 1, 'vote_detail_id': 1, 'points': ''}, {'ballot_id': 0, 'vote_id': 1, 'user_id': 1, 'vote_detail_id': 1, 'points': ''}, {'ballot_id': 0, 'vote_id': 1, 'user_id': 1, 'vote_detail_id': 1, 'points': ''}, {'ballot_id': 1, 'vote_id': 2, 'user_id': 1, 'vote_detail_id': 6, 'points': ''}, {'ballot_id': 1, 'vote_id': 2, 'user_id': 1, 'vote_detail_id': 6, 'points': ''}, {'ballot_id': 1, 'vote_id': 2, 'user_id': 1, 'vote_detail_id': 6, 'points': ''}, {'ballot_id': 1, 'vote_id': 2, 'user_id': 1, 'vote_detail_id': 6, 'points': ''}, {'ballot_id': 1, 'vote_id': 2, 'user_id': 1, 'vote_detail_id': 6, 'points': ''}, {'ballot_id': 1, 'vote_id': 2, 'user_id': 1, 'vote_detail_id': 6, 'points': ''}]

    # print([dict(b, points= 2 if b['vote_detail_id']) for b in ballot])
    # print([r for r in vote_detail if r['is_right'] == 'Y'])
    

if __name__ == "__main__":
    print("Launching Polls API")  
    # run_tests()
    uvicorn.run("main:app", port=3004, host="0.0.0.0", reload=True)