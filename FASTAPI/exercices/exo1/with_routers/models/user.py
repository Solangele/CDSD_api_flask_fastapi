from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional


class UserCreate(BaseModel):

    model_config = ConfigDict(from_attributes=True)


    username : str = Field(..., min_length= 2, max_length= 50, description= "User's name")
    email : EmailStr = Field(..., description= "User's mail address")
    age : Optional[int] = Field(None, ge = 0, le = 150, description= "User's age (0-150)")
    is_active : bool = Field(default= True, description= "Is user active ?")


class User(UserCreate):
    id : int = Field(..., description= "id autoincrement")