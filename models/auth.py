from pydantic import BaseModel
from typing import List

class TokenData(BaseModel):
    username: str = None
    roles: List[str] = []
    
class Token(TokenData):
    access_token: str
    token_type: str