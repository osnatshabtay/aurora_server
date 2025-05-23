from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    agreement: bool = True 
    selectedImage: str = None
    gender: str = 'אחר'



