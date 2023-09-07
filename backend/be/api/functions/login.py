from pydantic import BaseModel
from typing import Union
from passlib.context import CryptContext
from typing import Union
from jose import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer



# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "de77a09cf337758ac4ebc6060bf589a9f8ed48605b0276aecabd7043f74e2d75"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120 # 120分間トークンが有効
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#JWTトークンの取り扱い,トークンの定義
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
        # TODO: make user type to User Table
        user_dict = db[username]
        return user_dict


def authenticate_user(users_db, username: str, password: str):
    user = get_user(users_db, username)
    # userが登録されていなければ、errorが起きるようにする
    if not user:
        print("user is not registered")
        return False
    
    # passwordが違えば、errorが起きるようにする
    # TODO: make user type to User Table
    # user["Password"] => user.Password
    if not verify_password(password, user["password"]):
        print("Password is incorrect")
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
