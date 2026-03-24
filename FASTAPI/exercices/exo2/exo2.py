# ## Exercice 2: Validateurs Personnalisés

# **Énoncé**:
# Créez un modèle `Password` avec validation:
# - `password`: au moins 8 caractères, doit contenir minuscule, majuscule, chiffre, symbole
# - `confirm_password`: doit égaler `password`

# Retournez des erreurs détaillées si la validation échoue.

# Exemple:
# ```bash
# # Valide
# {"password": "SecurePass123!", "confirm_password": "SecurePass123!"}

# # Invalide
# {"password": "weak", "confirm_password": "weak"}
# # Erreur: "password too short"
# ```

from fastapi import FastAPI
from pydantic import BaseModel, field_validator, Field, ConfigDict, model_validator
from typing import Optional
import re


app = FastAPI(
    title="FastAPI exo2",
    description="password validation",
    version="1.0.0"
)

class Registration(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    username : str = Field(..., min_length= 2, max_length= 50, description= "User's name")
    password: str = Field(..., min_length=8, description="Password")
    confirm_password: str = Field(..., description="Confirm password")

    @field_validator('password')
    @classmethod
    def validate_password(cls, v) :
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v
    
    @model_validator(mode='after')
    def validate_passwords_match(self):
        """
        Root validator - validate across multiple fields
        Checks that password and confirm_password match
        """
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self

@app.post("/users", response_model=Registration)
async def create_user(user: Registration):
    return user