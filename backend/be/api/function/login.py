from pydantic import BaseModel
from typing import Union
from passlib.context import CryptContext
from typing import Union
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "de77a09cf337758ac4ebc6060bf589a9f8ed48605b0276aecabd7043f74e2d75"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 30分間トークンが有効
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
    if not verify_password(password, user["Password"]):
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

'''
 依存関係の更新
 get_current_userを更新して、先ほどと同じトークンを受け取るようにしますが、今回はJWTトークンを使用します。
 受け取ったトークンを復号して検証し、現在のユーザーを返します。
 トークンが無効な場合は、すぐにHTTPエラーを返します。
'''
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#         token_data = TokenData(username=email)
#     except JWTError:
#         raise credentials_exception
#     try:
#         users_dict = {}
#         users_list = session.query(UserTable).all()
#         for user in users_list:
#             email = user.Email
#             users_dict[email] = user.toDict()
#     except Exception as e:
#         print("This is post /token error")
#         print("Login api error")
#         print(e)

#     user = get_user(users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(current_user: UserHashPass = Depends(get_current_user)):
#     # if current_user.disabled:
#     #     raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

