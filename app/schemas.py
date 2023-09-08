from pydantic import BaseModel
from typing import List 

class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config():
        orm_mode = True

class GetUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

    class Config():
        orm_mode = True

class GetBlog(BaseModel):
    title: str
    body: str
    creator: GetUser
    class Config():
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str
