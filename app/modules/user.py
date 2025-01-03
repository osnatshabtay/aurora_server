from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    agreement: bool = True 
    selectedImage: str = None
    boy: bool = True


