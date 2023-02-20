import models
from fastapi import Depends, APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette import status
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user

router = APIRouter(
    prefix='/home',
    tags=['home'],
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


def get_user_masters(user_id: int, db: Session):
    return db.query(models.Masters).filter(models.Masters.owner_user_id == user_id).all()


@router.get('/', response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url='/auth', status_code=status.HTTP_302_FOUND)
    masters = get_user_masters(user.get('id'), db)
    if not masters:
        return RedirectResponse(url='/masters/new-master', status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse('home.html', {'request': request, 'user': user, 'masters': masters, 'servants': []})
