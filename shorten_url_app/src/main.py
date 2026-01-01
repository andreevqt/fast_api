import hashlib
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import select
from database import SessionDep, create_db_and_tables
from models import Url
from dto import UrlDto

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_tables()

def shorten_url(long_url):
    return hashlib.md5(long_url.encode()).hexdigest()[:14]

@app.post("/shorten/")
async def shorten_url(dto: UrlDto, session: SessionDep):
    shorten = shorten_url(dto.url)
    model = Url.model_validate(dto, update={"shorten": shorten, "full": dto.url})
    session.add(model)
    session.commit()
    return shorten

@app.get("/{shorten}")
async def process_url(shorten: str, session: SessionDep):
    model = session.exec(select(Url).where(Url.shorten == shorten)).first()
    if not model:
        raise HTTPException(status_code=404, detail="Url not found")

    return RedirectResponse(model.full);

@app.get("/stats/{shorten}")
async def get(shorten: str, session: SessionDep) -> Url:
    model = session.exec(select(Url).where(Url.shorten == shorten)).first()
    if not model:
        raise HTTPException(status_code=404, detail="Url not found")

    return model
