from pydantic import BaseModel
from typing import Optional # attribute not required to appear in the body request

class User(BaseModel):
    id: Optional[str] = None
    name: str
    age: Optional[int] = None