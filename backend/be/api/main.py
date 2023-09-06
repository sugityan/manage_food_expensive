from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db import session
from model import *
from pydantic import BaseModel
from datetime import datetime, timedelta
from function.login import *
from fastapi.responses import JSONResponse





app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 許可するオリジンのリスト
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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


# @app.post("/eatout_register")  # 適切なエンドポイント名に置き換えてください
# async def receive_data(data: EatoutData):
#     # 受け取ったデータをそれぞれの変数に格納
#     received_date = data.date
#     received_price = data.price
#     received_purpose = data.purpose

#     # ここで受け取ったデータを使って何かを実行できます。
#     # 今回はデモのため、受け取ったデータをそのままレスポンスとして返します。
#     return {
#         "received_date": received_date,
#         "received_price": received_price,
#         "received_purpose": received_purpose
#     }

@app.post("/eatout_register")
async def add_data(data: EatoutData):
    # 文字列をdatetime.dateに変換
    converted_date = datetime.strptime(data.date, "%Y-%m-%d").date()
    actual_db_item = Shopping(UserID=1, Date=converted_date, Price=data.price, Purpose=data.purpose)
    session.add(actual_db_item)
    session.commit()

    return {"message": "Data added successfully!"}
# ユーザ情報登録
# @app.post("/test_users")
# def post_user(user: TestUser):
#     db_test_user = TestUser(id=user.id,
#                             name=user.name,
#                             email=user.email)
#     actual_db_item = TestUserTable(** db_test_user.dict())
#     session.add(actual_db_item)
#     session.commit()
    

@app.post("/")
def post_user(user: UserCreate):
    actual_db_item = TestUserTable2(name=user.name, nickname=user.email)
    session.add(actual_db_item)
    session.commit()
    return{"result": 3}
    
    

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

@app.get("/users")
def get_users():
    users = session.query(UserTable).all()
    return users

@app.post("/users")
def create_user(user: User):
    actual_db_item = UserTable(UserID=user.userID, Password=get_password_hash(user.password), p_num=user.p_num, age=user.age, Email=user.email)
    session.add(actual_db_item)
    session.commit()
    return UserTable(UserID=user.userID, Password=user.password, p_num=user.p_num, age=user.age, Email=user.email)
    
@app.get("/get_users_dict")
def get_users_dict():
    users_dict = {}
    users_list = session.query(UserTable).all()
    for user in users_list:
        email = user.Email
        users_dict[email] = user.toDict()
    return users_dict

"""
login API
""" 

'''
/token パスオペレーションの更新¶
トークンの有効期限を表すtimedeltaを作成します。

JWTアクセストークンを作成し、それを返します。
'''
@app.post("/token", response_model=Token)
# First, import OAuth2PasswordRequestForm, and use it as a dependency with Depends in the path operation for /token:
# TODO: form_data => json from frontend input
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print("login_for_access_token api message")
    print("TODO: change form_data to json from frontend input")
    # Get users from mysql db:
    try:
        users_db = get_users_dict()
    except Exception as e:
        print("This is post /token error")
        print("Login api error")
        print(e)

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
    print(user)
    access_token = create_access_token(
        # TODO: make user type to User Table
        # user["user"] => user.Email
        data={"sub": user["Email"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


# @app.get("/users/me/", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user


# @app.get("/users/me/items/")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     # TODO
#     # current_user.username => current_user.email
#     return [{"item_id": "Foo", "owner": current_user.email}]