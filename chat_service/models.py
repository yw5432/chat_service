from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class GroupCreate(BaseModel):
    group_name: str
    created_by: str

class JoinRequest(BaseModel):
    username: str
    group_name: str
