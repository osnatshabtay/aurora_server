from pydantic import BaseModel, Field
from typing import Set, List, Dict, Optional
from datetime import datetime


class Comment(BaseModel):
    username: str 
    text: str 
    timestamp: datetime = Field(default_factory=datetime.utcnow) 
    approved : bool = False


class Post(BaseModel):
    user: str = None
    user_image: str = None
    text: str
    mood: Optional[str] = None
    likes: List[str] = Field(default_factory=list)
    commands: List[Comment] = Field(default_factory=list)
    approved : bool = False

class LikeRequest(BaseModel):
    post_id: str

class CommentRequest(BaseModel):
    post_id: str
    text: str
