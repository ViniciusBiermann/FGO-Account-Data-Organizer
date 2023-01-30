import models
import requests
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from starlette.staticfiles import StaticFiles
from starlette import status
from starlette.responses import RedirectResponse
from routers import home, auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get("/")
async def root():
    return RedirectResponse(url='/home', status_code=status.HTTP_302_FOUND)


app.include_router(home.router)
app.include_router(auth.router)


@app.get('/updateServants')
async def update_servants_table(db: Session = Depends(get_db)):
    url = 'https://api.atlasacademy.io/export/JP/basic_servant_lang_en.json'
    r = requests.get(url, allow_redirects=True)
    servant_classes = {
        'saber': 'Saber',
        'archer': 'Archer',
        'lancer': 'Lancer',
        'rider': 'Rider',
        'caster': 'Caster',
        'assassin': 'Assassin',
        'berserker': 'Berserker',
        'ruler': 'Ruler',
        'avenger': 'Avenger',
        'moonCancer': 'Moon Cancer',
        'alterEgo': 'Alter Ego',
        'foreigner': 'Foreigner',
        'pretender': 'Pretender',
        'shielder': 'Shielder'
    }
    for servant in r.json():
        if servant.get('className') not in servant_classes.keys():
            continue
        servant_id = int(servant.get('collectionNo'))
        servant_model = db.query(models.Servants).filter(models.Servants.id == servant_id).first()
        if servant_model is None:
            servant_model = models.Servants()
        servant_model.id = servant_id
        servant_model.name = servant.get('name')
        servant_model.name_jp = servant.get('originalName')
        servant_model.servant_class = servant_classes.get(servant.get('className'))
        servant_model.rarity = servant.get('rarity')
        db.add(servant_model)
    db.commit()
    return {"message": "Successful"}
