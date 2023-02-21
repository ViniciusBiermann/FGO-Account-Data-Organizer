import models
from fastapi import Depends, APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette import status
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user
from datetime import datetime

router = APIRouter(
    prefix='/masters',
    tags=['masters'],
    responses={404: {'description': 'Not found.'}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory='templates')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/new-master', response_class=HTMLResponse)
async def add_new_master(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse('new-master.html', {'request': request, 'user': user})


@router.post('/new-master', response_class=HTMLResponse)
async def create_master(request: Request,
                        in_game_id: str = Form(),
                        master_name: str = Form(),
                        gender: str = Form(),
                        birthday_month: int = Form(),
                        birthday_day: int = Form(),
                        master_level: int = Form(),
                        saint_quartz: int = Form(),
                        paid_saint_quartz: int = Form(),
                        rare_prisms: int = Form(),
                        spirit_origin: int = Form(),
                        download: str = Form(),
                        last_access: str = Form(),
                        device: str = Form(),
                        recovery_number: str = Form(),
                        db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    master_model = models.Masters()
    master_model.owner_user_id = user.get('id')
    master_model.in_game_id = in_game_id
    master_model.name = master_name
    master_model.gender = gender
    master_model.birthday = f"{birthday_day}/{birthday_month}"
    master_model.master_level = master_level
    master_model.saint_quartz = saint_quartz
    master_model.paid_saint_quartz = paid_saint_quartz
    master_model.rare_prisms = rare_prisms
    master_model.unregistered_spirit_origin = spirit_origin
    master_model.download_date = datetime.strptime(download, '%Y-%m-%d').date()
    master_model.last_access = datetime.strptime(last_access, '%Y-%m-%dT%H:%M')
    master_model.device = device
    master_model.recovery_number = recovery_number

    db.add(master_model)
    db.commit()

    return RedirectResponse(url='/home', status_code=status.HTTP_302_FOUND)


@router.get('/{master_id}')
async def get_master_by_id(request: Request, master_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return None
    master = db.query(models.Masters).filter(models.Masters.owner_user_id == int(user.get('id'))).filter(
        models.Masters.id == master_id).first()
    return master


@router.get('/{master_id}/servants')
async def get_master_servants(request: Request, master_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return None
    master = db.query(models.Masters).filter(models.Masters.owner_user_id == int(user.get('id'))).filter(
        models.Masters.id == master_id).first()
    if master is None:
        return None
    servants = master.servants
    return servants
