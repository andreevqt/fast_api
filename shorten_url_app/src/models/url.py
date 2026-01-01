from sqlmodel import Field, SQLModel

class Url(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    full: str
    shorten: str
