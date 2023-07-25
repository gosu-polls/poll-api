from fastapi import Request
import json
import jwt

usersList = []

def prime_users():
    global usersList 
    usersList = [
        {
            "name" : "Kiran Gosu",
            "email" : "kirankumar.gosu@gmail.com"
        },
        {
            "name" : "Ramya Chellamuthu",
            "email" : "ramya2202@gmail.com"
        },
        {
            "name" : "Dhruv Kiran Gosu",
            "email" : "dhruvkgosu@icloud.com"
        }
    ] 
def get_user(request: Request) -> dict:
    global usersList
    header = json.loads(request.headers.get('Token'))
    # print(header)
    user = None
    if header != None:
        email = jwt.decode(header['jwt'], 'secret', 'HS256')['email']
        # print(f'get_user email is {email}')

        if len(usersList) == 0:
            prime_users()
        
        userList = [u for u in usersList if u['email'] == email]
        user = userList[0]
    return user
    