import requests
import jwt
from src.db.cwc.cosmos.user import User as User

def handle_user(user : dict) -> dict:
    headers = {'Authorization': 'Bearer' + user['user']['access_token'],
               'Accept': 'application/json'}
    response = requests.get(url = 'https://www.googleapis.com/oauth2/v1/userinfo', 
                            headers = headers)
    encoded_jwt = jwt.encode(payload = {"email": response.json()['email']}, 
                             key = "secret", 
                             algorithm="HS256")
    userdata = response.json()
    userdata['jwt'] = encoded_jwt
    # print(userdata)

    # {'id': '117242629996049838225', 
    #  'email': 'kirankumar.gosu@gmail.com', 
    #  'verified_email': True, 
    #  'name': 'Kiran Gosu', 
    #  'given_name': 'Kiran', 
    #  'family_name': 'Gosu', 
    #  'picture': 'https://lh3.googleusercontent.com/a/AAcHTtebPZq-IT9DjR2sQJP5Yl2ziMSbqR01tawoINV4HFNu2paO=s96-c', 'locale': 'en-GB', 'jwt': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImtpcmFua3VtYXIuZ29zdUBnbWFpbC5jb20ifQ.-A4p8lFWslLUEAX37Yvr6m1bBhRgEQOtwnWaNBKtG5g'}
    User().AddUser(userdata)
    return userdata