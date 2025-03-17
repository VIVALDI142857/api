from fastapi import FastAPI
import pydantic
from pydantic import BaseModel, Field, EmailStr, ConfigDict
import pandas as pd
import requests as r

app = FastAPI()


class User(BaseModel):
    name: str
    age: int = Field(ge=0, le=130)
    email: EmailStr 
    
    model_config = ConfigDict(extra='forbid')

df = {"name": "Alice", "age": 33, 'email': 'alice@gmail.com'}
users = []

@app.get('/')
def home():
    return {'message': 'Hello!'}

@app.get('/square/{number}')
def square(number: int):
    return {'squared number': number ** 2}

@app.post('/reverse/{text}')
def rev(text: str):
    return {'reversed_text' : text[::-1]}

@app.post('/users')
def add_user(user:User):
    users.append(user)
    return {'success': True}

@app.get('/users')
def get_users():
    return users
    

print(User(**df))
