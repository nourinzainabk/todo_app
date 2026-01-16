from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str
    completed: bool

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        from_attributes = True

