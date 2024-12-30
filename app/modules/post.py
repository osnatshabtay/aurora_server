from pydantic import BaseModel, Field
from typing import Set, List, Dict
from datetime import datetime


class Comment(BaseModel):
    username: str 
    text: str 
    timestamp: datetime = Field(default_factory=datetime.utcnow)  # Time of comment


class Post(BaseModel):
    username: str
    text: str
    likes: Set[str] = Field(default_factory=set)
    commands: List[Comment] = Field(default_factory=list)
    approved : bool = False
