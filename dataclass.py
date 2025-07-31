from dataclasses import dataclass
from pydantic import BaseModel

# @dataclass
# class User:
#     name:str
#     id:int

class User(BaseModel):
    name:str
    id:str

def get_name(user:User):
    print(user.name)
    print(user.id)

get_name("bilal", 1) #for dataclass
get_name(name="bilal",id=1) # for pydantic

#Assignment:  Learn How to validate data using pydantic 