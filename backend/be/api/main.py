from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import session
from model import *
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import datetime

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


#　ログイン画面：ユーザー情報一覧取得
@app.get("/get_users_dict")
def get_users_dict():
    users_dict = {}
    users_list = session.query(User).all()
    for user in users_list:
        email = user.Email
        users_dict[email] = user
    return users_dict
"""

# ユーザ登録画面：ユーザ情報登録
@app.post("/sign_up_user")
def post_user(user: User):
    new_user = User(email=user.email,
                        age=user.age,
                        household=user.household,
                        password=user.password)
    session.add(new_user)
    session.commit()


# 食材登録画面：食材登録
@app.post("/add_food")
def post_food(food: Food):
    new_food = Food(food_name=food.food_name,
                        category=food.category,
                        price=food.price,
                        limit_date=food.limit_date,
                        buy_date=food.buy_date,
                        amount=food.amount,
                        unit=food.unit,
                        memo=food.memo,
                        remain_ratio=food.remain_ratio,
                        userID=food.userID)
    session.add(new_food)
    session.commit()

# 食費登録画面：食費情報登録
@app.post("/add_cost")
def post_cost(cost: Cost):
    new_cost = Cost(buy_date=cost.buy_date,
                        uses=cost.uses,
                        price=cost.price,
                        userID=cost.userID)
    session.add(new_cost)
    session.commit()

# 食材一覧画面：食材情報一覧取得
@app.get("/get_foods")
def get_food_list():
    users = session.query(UserTable).all()
    return users
"""