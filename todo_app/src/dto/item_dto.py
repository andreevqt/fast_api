from sqlmodel import SQLModel

class ItemDto(SQLModel):
    title: str
    description: str
