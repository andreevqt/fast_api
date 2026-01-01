from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:////app/data/app.db"

def get_session():
    with Session(engine) as session:
        yield session

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
