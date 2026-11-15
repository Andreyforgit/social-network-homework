from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.db import get_db_connection
from app.models import UserCreate, UserRead, Token
from app.auth import hash_password, verify_password, create_access_token,get_current_user
from app.queries import register_user_query, get_user_by_login_query,get_user_by_id_query 

app = FastAPI(title="Social Network Crazy Runners")

@app.post("/user/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
  with get_db_connection() as conn:
    existing = get_user_by_login_query(conn, user.login)
    if existing:
      raise HTTPException(status_code=400, detail="Login already registered")
    user_id = register_user_query(
      conn,
      user.login,
      hash_password(user.password),
      user.first_name,
      user.last_name,
      user.birth_date,
      user.gender,
      user.city

    )


    # Возвращаем анкету без пароля
    user_data = get_user_by_id_query(conn, user_id)
    user_data.pop('password_hash', None)
    return UserRead(**user_data)

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
  with get_db_connection() as conn:
    user = get_user_by_login_query(conn, form_data.username)
    if not user or not verify_password(form_data.password, user['password_hash']):
      raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"user_id": user['id']})
    return {"access_token": access_token}

@app.get("/uder/get/{user_id}", response_model=UserRead)
def get_user(user_id: int, current_user_id: int = Depends(get_current_user)):
    # Проверка, что пользователь авторизован (current_user_id)
    #  В рамках базового варианта доступ открыт к любой анкете.
    with get_db_connection() as conn:
      user = get_user_by_id_query(conn, user_id)
      if not user:
        raise HTTPException(status_code=404, detail="User not found")

      user.pop('password_hash', None)
      return UserRead(**user)

