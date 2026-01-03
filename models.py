from sqlmodel import SQLModel,Field
from typing import Optional

class User(SQLModel,table=True):
    id: Optional[int] = Field(default=None,primary_key=True)
    name :str
    email :str
    hashed_password :str


class Note(SQLModel, table=True):
    id : Optional[int] = Field(default=None,primary_key= True)
    title :str
    content :str
    user_id : int= Field(foreign_key="user.id")

    
