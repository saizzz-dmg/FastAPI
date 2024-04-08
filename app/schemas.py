from pydantic import BaseModel , EmailStr, conint
from datetime import datetime
from typing import Optional

class posts(BaseModel):
    title : str
    post : bool = True
    content: str
    user_id : int

class Updateposts(posts):
    class Config:
        form_attributes = True

class UserOut(BaseModel):
    id : int
    email:str
    created_at : datetime

class displayPosts(BaseModel):
    id : int
    title:str
    post:  bool
    content : str
    created_at: datetime
    user_id : int
    owner : UserOut

class postOut(BaseModel):
    post : displayPosts
    votes : int


    
    
class User(BaseModel):
    password : str
    email : EmailStr



class verify_user(BaseModel):
    password: str
    class Config:
        form_attributes = True

class authentication(BaseModel):
    email: EmailStr
    password : str

class authout(BaseModel):
    email : EmailStr
    created_at : datetime
    id : int

class Tokendata(BaseModel):
    id : Optional[str] = None

class Token(BaseModel):
    id : str
    user_id : int
    token_type : str = "Bearer"

class Vote(BaseModel):
    post_id : int
    vote_dir : int



    





    
