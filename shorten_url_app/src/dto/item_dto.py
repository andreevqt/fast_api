from sqlmodel import SQLModel

class UrlDto(SQLModel):
    url: str
