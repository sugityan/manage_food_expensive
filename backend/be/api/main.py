# from fastapi import Depends, FastAPI
# from db import session
# from model import *
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from typing_extensions import Annotated


# app = FastAPI()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# #　ユーザー情報一覧取得
# @app.get("/test_users")
# def get_user_list():
#     users = session.query(TestUserTable).all()
#     return users


# # ユーザー情報取得(id指定)
# @app.get("/test_users/{user_id}")
# def get_user(user_id: int):
#     user = session.query(TestUserTable).\
#         filter(TestUserTable.id == user_id).first()
#     return user


# # ユーザ情報登録
# @app.post("/test_users")
# def post_user(user: TestUser):
#     db_test_user = TestUser(id=user.id,
#                             name=user.name,
#                             email=user.email)
#     actual_db_item = TestUserTable(** db_test_user.dict())
#     session.add(actual_db_item)
#     session.commit()
    
    



# # ユーザ情報登録
# @app.get("/users")
# def get_user_list():
#     users = session.query(UserTable).all()
#     return users

# @app.post("/user")
# def user(user: User):
#     db_user = User(
#         userId=user.userID,
#         email=user.email,
#         age=user.age,
#         household=user.household,
#         password=user.password
#     )
#     db_user = UserTable(** db_user.dict())
#     session.add(db_user)
#     session.commit()

# # def fake_decode_token(token):
# #     return User(
# #         userID=1 , mail=token + "fakedecoded", age=1, household=1, password="password"
# #     )

# # async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
# #     user = fake_decode_token(token)
# #     return user


# # # ログイン
# # @app.get("/user/login")
# # async def login(token: Annotated[User, Depends(get_current_user)]):
# #     return token



# # ユーザ情報更新
# @app.put("/test_users/{user_id}")
# def put_users(user: TestUser, user_id: int):
#     target_user = session.query(TestUserTable).\
#         filter(TestUserTable.id == user_id).first()
#     target_user.name = user.name
#     target_user.email = user.email
#     session.commit()




from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "de77a09cf337758ac4ebc6060bf589a9f8ed48605b0276aecabd7043f74e2d75"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 30分間トークンが有効

users_db = {
    "test": {
        "userID": 1,
        "email": "test",
        "age": 1,
        "household": 1,
        "password": "password",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    },
}



#JWTトークンの取り扱い,トークンの定義
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    userID: int
    email: str
    age: int
    household: int
    password: str


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

#パスワードの検証
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#パスワードのハッシュ化
def get_password_hash(password):
    return pwd_context.hash(password)


# userが登録されているか確認
# userが登録されていなければ、nullを返す
# TODO: username => email
def get_user(db, username: str):
    if username in db:
        # db[username] => db
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    # userが登録されていなければ、errorが起きるようにする
    if not user:
        return False
    # userが登録されていなければ、errorが起きるようにする
    if not verify_password(password, user.hashed_password):
        return False
    return user

#JWTトークンの取り扱い,トークンの作成
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

'''
 依存関係の更新
 get_current_userを更新して、先ほどと同じトークンを受け取るようにしますが、今回はJWTトークンを使用します。
 受け取ったトークンを復号して検証し、現在のユーザーを返します。
 トークンが無効な場合は、すぐにHTTPエラーを返します。
'''
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # TODO: check payload
        print("This is payload")
        print(payload)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # TODO: users_db => db from mysql
    user = get_user(users_db, username=token_data.username)
    # user = get_user(true_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


'''
/token パスオペレーションの更新¶
トークンの有効期限を表すtimedeltaを作成します。

JWTアクセストークンを作成し、それを返します。
'''
@app.post("/token", response_model=Token)
# First, import OAuth2PasswordRequestForm, and use it as a dependency with Depends in the path operation for /token:
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # TODO
    # fake_users_db => db from MySql
    user = authenticate_user(users_db, form_data.username, form_data.password)
    # user = authenticate_user(true_users_db, form_data.username, form_data.password)
    if not user: # When user is False, return HTTPException
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # tokenの期限を設定
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # tokenの作成
    access_token = create_access_token(
        # TODO
        # user.username => user.email
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    # TODO
    # current_user.username => current_user.email
    return [{"item_id": "Foo", "owner": current_user.email}]
