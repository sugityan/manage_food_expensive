from fastapi import Depends, FastAPI
from db import session
from model import *
from fastapi.security import OAuth2PasswordBearer


app = FastAPI()

#　ユーザー情報一覧取得
@app.get("/test_users")
def get_user_list():
    users = session.query(TestUserTable).all()
    return users


# ユーザー情報取得(id指定)
@app.get("/test_users/{user_id}")
def get_user(user_id: int):
    user = session.query(TestUserTable).\
        filter(TestUserTable.id == user_id).first()
    return user


# ユーザ情報登録
@app.post("/test_users")
def post_user(user: TestUser):
    db_test_user = TestUser(id=user.id,
                            name=user.name,
                            email=user.email)
    actual_db_item = TestUserTable(** db_test_user.dict())
    session.add(actual_db_item)
    session.commit()
    
    

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # ユーザ情報登録
# @app.post("/users")
# def user(user2: User):
#     db_user = User(
#                    name=user2.name,
#                     email=user2.email,
#                     password=user2.password)
#     session.add(db_user)
#     session.commit()

# # ログイン
# @app.get("/users/login")
# async def login(token: str = Depends(oauth2_scheme)):
#     return {"token": token}



# ユーザ情報更新
@app.put("/test_users/{user_id}")
def put_users(user: TestUser, user_id: int):
    target_user = session.query(TestUserTable).\
        filter(TestUserTable.id == user_id).first()
    target_user.name = user.name
    target_user.email = user.email
    session.commit()

