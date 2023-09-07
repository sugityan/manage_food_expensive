from pydantic import BaseModel
from typing import Union
from passlib.context import CryptContext
from typing import Union
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from .login import *
from main import *

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
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(username=email)
    except JWTError:
        raise credentials_exception
    try:
        users_dict = {}
        users_list = session.query(UserTable).all()
        for user in users_list:
            email = user.Email
            users_dict[email] = user.toDict()
    except Exception as e:
        print("This is post /token error")
        print("Login api error")
        print(e)

    users_db = get_users_dict()
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return loginUser(**user)
