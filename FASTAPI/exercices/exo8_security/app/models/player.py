from enum import Enum

from sqlalchemy import Boolean, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship, sessionmaker, Session
from typing import Generator

from app.core.database import Base



# -----------------------------------------------------------------------------
# Configuration SQLAlchemy
# -----------------------------------------------------------------------------

DATABASE_URL = "sqlite:///./relations_demo_v2.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------------------------------------------------------
# Modèle 1 : Les joueurs
# -----------------------------------------------------------------------------
class Players(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key= True, index= True)
    nickname: Mapped[str] = mapped_column(String(50), unique= True, index= True, nullable= False)
    first_name: Mapped[str] = mapped_column(String(250), unique= False, nullable= False)
    last_name: Mapped[str] = mapped_column(String(250), unique= False, nullable= False)



# -----------------------------------------------------------------------------
# Modèle 2 : Les équipes
# -----------------------------------------------------------------------------
class Teams(Base): 
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key= True, index= True)
    name: Mapped[str] = mapped_column(String(50), unique= True, nullable= False)
    player_1_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"), nullable= False)
    player_2_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"), nullable= False)

    player_1 = relationship("Players", foreign_keys=[player_1_id])
    player_2 = relationship("Players", foreign_keys=[player_2_id])



# -----------------------------------------------------------------------------
# Modèle 3 : Les matchs
# -----------------------------------------------------------------------------

class MatchTypes(str, Enum):
    SINGLE = "single"
    TEAM = "team"

class Matches(Base): 
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(Integer, primary_key= True, index= True)
    match_type: Mapped[str] = mapped_column(String(10), default= MatchTypes.SINGLE.value, nullable= False)
    player_1_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("players.id"), nullable=True)
    team_1_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("teams.id"), nullable=True)
    player_2_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("players.id"), nullable=True)
    team_2_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("teams.id"), nullable=True)
    score_1: Mapped[int] = mapped_column(Integer, nullable= False)
    score_2: Mapped[int] = mapped_column(Integer, nullable= False)

    player_1 = relationship("Players", foreign_keys= [player_1_id])
    player_2 = relationship("Players", foreign_keys= [player_2_id])
    team_1 = relationship("Teams", foreign_keys= [team_1_id])
    team_2 = relationship("Teams", foreign_keys= [team_2_id])



# -----------------------------------------------------------------------------
# Création des tables
# -----------------------------------------------------------------------------

Base.metadata.create_all(bind=engine)



# -----------------------------------------------------------------------------
# Données de démonstration
# -----------------------------------------------------------------------------

def seed_data() -> None:
    """
    Insère quelques données si la base est vide.

    On crée :
    - 7 joueurs
    - 4 équipes

    Cela permet de démarrer la démo immédiatement sans avoir à faire de POST.
    """
    db: Session = SessionLocal()
    try:
        existing_authors = db.query(Players).count()
        if existing_authors > 0:
            return

        player_1 = Players(nickname="Bob", first_name="Bobby", last_name="Bob")
        player_2 = Players(nickname="Jony", first_name="John", last_name="John")
        player_3 = Players(nickname="Lulu", first_name="Lucie", last_name="Liu")
        player_4 = Players(nickname="Toto", first_name="Tom", last_name="Tom")
        player_5 = Players(nickname="Momo", first_name="Maurice", last_name="Mau")
        player_6 = Players(nickname="Tutu", first_name="Tu", last_name="Tu")
        player_7 = Players(nickname="Mimi", first_name="Mi", last_name="Mi")

        db.add_all([player_1, player_2, player_3, player_4, player_5, player_6, player_7])
        db.commit()
        db.refresh(player_1)
        db.refresh(player_2)
        db.refresh(player_3)
        db.refresh(player_4)
        db.refresh(player_5)
        db.refresh(player_6)
        db.refresh(player_7)

        team_1 = Teams(
            name="Team A",
            p1_player_id=player_1.id,
            p2_player_id=player_2.id,
        )

        team_2 = Teams(
            name="Team B",
            p1_player_id=player_3.id,
            p2_player_id=player_4.id,
        )

        team_3 = Teams(
            name="Team C",
            p1_player_id=player_5.id,
            p2_player_id=player_6.id,
        )

        team_4 = Teams(
            name="Team D",
            p1_player_id=player_7.id,
            p2_player_id=player_5.id,
        )

        db.add_all([team_1, team_2, team_3, team_4])
        db.commit()
    finally:
        db.close()


seed_data()

