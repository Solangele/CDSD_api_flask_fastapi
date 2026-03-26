from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

db_path_str = os.getenv("DATABASE_PATH", "data/app.db")
db_path = Path(db_path_str)

db_path.parent.mkdir(parents= True, exist_ok= True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path.resolve()}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

Base = declarative_base()