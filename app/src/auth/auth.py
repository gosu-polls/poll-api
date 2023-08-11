import requests
import jwt
from datetime import datetime

from src.database.db.poll.user import User as User

def handle_user(user : dict) -> dict:
    headers = {'Authorization': 'Bearer' + user['user']['access_token'],
               'Accept': 'application/json'}
    response = requests.get(url = 'https://www.googleapis.com/oauth2/v1/userinfo', 
                            headers = headers)
    encoded_jwt = jwt.encode(payload = {"email": response.json()['email']}, 
                             key = "secret", 
                             algorithm="HS256")
    userData = response.json()
    userData['jwt'] = encoded_jwt

    users = User().GetData()
    if (userData['email'] in [u['email'] for u in users]):
        set_clause = {'last_logged_on': datetime.now().strftime("%Y-%m-%d %H%M%S")}
        where_clause = {'email': userData['email']}
        User().UpdateData(set_clause=set_clause, where_clause=where_clause)
    else:
        # new_user = {'user_id': User().GetNextId(),
        #             'email': userData['email'],
        #             'joined_on': datetime.now().strftime("%Y-%m-%d %H%M%S"),
        #             'last_logged_on': datetime.now().strftime("%Y-%m-%d %H%M%S")
        #            }
        new_user = {'email': userData['email'],
                    'joined_on': datetime.now().strftime("%Y-%m-%d %H%M%S"),
                    'last_logged_on': datetime.now().strftime("%Y-%m-%d %H%M%S")
                   }
        User().AddData(new_user)
    return userData