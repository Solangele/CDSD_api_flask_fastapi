
# ## Exercice 1: Modèle Utilisateur Basique

# **Énoncé**:
# Créez un modèle Pydantic `User` avec:
# - `id`: entier (non modifiable)
# - `username`: chaîne (2-50 caractères)
# - `email`: email valide
# - `age`: entier optionnel (0-150 si fourni)
# - `is_active`: booléen (par défaut True)

# Testez avec une route POST `/users` qui accepte le modèle.

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

app = FastAPI(
    title="FastAPI exo1",
    description="user validation",
    version="1.0.0"
)

class UserSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)


    id : int
    username : str = Field(..., min_length= 2, max_length= 50, description= "User's name")
    email : EmailStr = Field(..., description= "User's mail address")
    age : Optional[int] = Field(None, ge = 0, le = 150, description= "User's age (0-150)")
    is_active : bool = Field(default= True, description= "Is user active ?")



@app.post("/users", response_model=UserSchema)
async def create_user(user: UserSchema):
    return user 