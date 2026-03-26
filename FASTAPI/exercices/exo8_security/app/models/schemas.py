from pydantic import BaseModel, Field

class PlayerRegister(BaseModel):
    nickname: str = Field(..., min_length= 3, max_length= 15)
    first_name: str = Field(..., min_length= 2, max_length= 50)
    last_name: str = Field(..., min_length= 2, max_length= 50)


class PlayerLogin(BaseModel):
    nickname: str
    password: str


class PlayerPublic(BaseModel):
    id: int
    nickname: str
    first_name: str
    last_name: str


class TeamsRegister(BaseModel):
    name: str
    player_1_id: int
    player_2_id: int


class TeamsPublic(BaseModel):
    id: int
    player_1: str
    player_2: str


class MatchesRegister(BaseModel):
    match_type: str
    player_1_id: int
    team_1_id: int
    player_2_id: int
    team_2_id: int
    score_1: int
    score_2: int
    

