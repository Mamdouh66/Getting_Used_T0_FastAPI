from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str

class GetBlog(Blog):
    class Config():
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str

class GetUser(BaseModel):
    name: str
    email: str
    class Config():
        orm_mode = True