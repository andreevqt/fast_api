from fastapi import FastAPI, HTTPException
from sqlmodel import select
from database import SessionDep, create_db_and_tables
from models import Item
from dto import ItemDto

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_tables()

@app.get("/items/")
async def list_items(session: SessionDep) -> list[Item]:
    return session.exec(select(Item)).all()

@app.post("/items/")
async def create_item(dto: ItemDto, session: SessionDep) -> Item:
    model = Item.model_validate(dto)
    session.add(model)
    session.commit()
    session.refresh(model)
    return model

@app.put("/items/{item_id}")
async def update_item(item_id: int, dto: ItemDto, session: SessionDep) -> Item:
    model = session.get(Item, item_id)
    if not model:
        raise HTTPException(status_code=404, detail="Item not found")

    update_data = dto.model_dump(exclude_unset=True)
    model.sqlmodel_update(update_data)
    session.add(model)
    session.commit()
    session.refresh(model)
    return model

@app.get("/items/{item_id}")
async def read_item(item_id: int, session: SessionDep) -> Item:
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/items/{item_id}")
async def read_item(item_id: int, session: SessionDep):
    model = session.get(Item, item_id)
    if not model:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(model)
    session.commit()
    return {"ok": True}
