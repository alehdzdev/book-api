from datetime import timedelta, datetime

# FastAPI
from fastapi import APIRouter, HTTPException, status, Depends, Form


# Local
from auth.models import Token, UserCreate, User
from auth.services import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_user,
    get_user,
)
from config import settings
from db.mongo import get_database


router = APIRouter(prefix="/auth", tags=["authentication"])


class LoginRequestForm:
    def __init__(self, username: str = Form(...), password: str = Form(...)):
        self.username = username
        self.password = password


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    db = get_database()

    existing_user = get_user(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    user_dict = {
        "username": user.username,
        "hashed_password": get_password_hash(user.password),
        "created_at": datetime.utcnow(),
    }

    result = db.users.insert_one(user_dict)
    created_user = db.users.find_one({"_id": result.inserted_id})

    return User(
        id=str(created_user["_id"]),
        username=created_user["username"],
    )


@router.post("/login", response_model=Token)
async def login(form_data: LoginRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def get_current_user_info(current_user=Depends(get_current_user)):
    return User(id=current_user.id, username=current_user.username)
