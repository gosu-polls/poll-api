from fastapi import FastAPI, Request
from requests import request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import src.auth.auth as auth
# import json
# import jwt
import src.facade as facade
# from src.db.student import Student as Student
from src.database.db.test.match import Match as Match
from src.database.db.test.country import Country as Country
from src.database.db.poll.group import Group as Group

from src.database.db.test.cosmos.country_v2 import Country as Country_v2
from src.database.db.test.cosmos.user import User as User

import functools
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:3000",
    "http://localhost:3001",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Polls": "Root"}

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
#     return src.polls.get_active_poll()

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
        return {"exception": err}
    
@app.get("/matches/{id}")
def get_match(id : int) -> dict:
    try:
        data = Match().GetDatum(id)
        return {"data": data}
    except Exception as err:
        return {"exception": err}
        
@app.get("/countries")
def get_countries() -> dict:
    try:
        data = Country().GetData()
        return {"data": data}
    except Exception as err:
        return {"exception": err}
    
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
def get_available_polls(request: Request) -> dict:
    data = facade.get_groups_admin(request)
    return data

@app.get("/participatingpolls")
def get_participating_polls(request: Request) -> dict:
    data = facade.get_participating_polls(request)
    return data

@app.get("/poll")
def get_poll(request: Request) -> dict:
    data = facade.get_active_poll(request)
    return data

@app.get("/pollhistory")
def get_poll_history(request: Request) -> dict:
    data = facade.get_poll_history(request)
    return data

if __name__ == "__main__":
    print("Launching Polls API")
    uvicorn.run("main:app", port=3003, host="0.0.0.0", reload=True)