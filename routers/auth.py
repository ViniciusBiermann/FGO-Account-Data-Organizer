from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form
from typing import Optional
from passlib.context import CryptContext
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import models

SECRET_KEY = "C&E)H@McQfTjWnZr4u7x!A%D*G-JaNdR"
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')

templates = Jinja2Templates(directory='templates')

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={401: {'user': 'Not authorized.'}}
)


class LoginForm:
    def __init__(self, request: Request):
        self.request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get('username')
        self.password = form.get('password')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password: str):
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user or not verify_password(password, user.password):
        user = db.query(models.Users).filter(models.Users.email == username).first()
        if not user or not verify_password(password, user.password):
            return None
    elif not verify_password(password, user.password):
        return None
    return user


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {'sub': username, 'id': user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(request: Request):
    try:
        token = request.cookies.get('access_token')
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            await logout(request)
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=404, detail='Not Found')


@router.post('/token')
async def login_for_access_token(response: Response, form_data: LoginForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if user is None:
        return False
    token_expires = timedelta(minutes=60)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)
    response.set_cookie(key='access_token', value=token, httponly=True)
    return True


@router.get('/', response_class=HTMLResponse)
async def authentication_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.post('/', response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url='/home', status_code=status.HTTP_302_FOUND)
        validate_user_cookie = await login_for_access_token(response=response, form_data=form, db=db)

        if not validate_user_cookie:
            message = 'Invalid Username or Password'
            return templates.TemplateResponse('login.html', {'request': request, 'msg': message})
        return response
    except HTTPException:
        message = 'Unknown Error'
        return templates.TemplateResponse('login.html', {'request': request, 'msg': message})


@router.get('/logout', response_class=HTMLResponse)
async def logout(request: Request):
    message = 'Logout Successful'
    response = templates.TemplateResponse('login.html', {'request': request, 'msg': message})
    response.delete_cookie(key='access_token')
    return response


@router.get('/register', response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})


@router.post('/register', response_class=HTMLResponse)
async def register_user(request: Request, email: str = Form(), username: str = Form(), password: str = Form(), password2: str = Form(),
                        db: Session = Depends(get_db)):
    message = 'Invalid registration request. An account with email or username already exists.'
    response_template = 'register.html'
    if password == password2:
        validation_1 = db.query(models.Users).filter(models.Users.username == username).first()
        validation_2 = db.query(models.Users).filter(models.Users.email == email).first()
        if not validation_1 and not validation_2:
            user_model = models.Users()
            user_model.username = username
            user_model.email = email
            user_model.password = get_password_hash(password)

            db.add(user_model)
            db.commit()

            message = 'User successfully created'
            response_template = 'login.html'

    return templates.TemplateResponse(response_template, {'request': request, 'msg': message})
