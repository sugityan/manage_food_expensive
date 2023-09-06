from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import session
from model import *
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 許可するオリジンのリスト
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ユーザ情報登録
@app.post("/test_users")
def post_user(user: TestUser):
    db_test_user = TestUser(name=user.name,
                            email=user.email)
    session.add(db_test_user)
    session.commit()

#　ユーザー情報一覧取得
@app.get("/test_users")
def get_user_list():
    users = session.query(UserTable).all()
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
    converted_date = datetime.datetime.strptime(data.date, "%Y-%m-%d").date()
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
    users_list = session.query(UserTable).all()
    for user in users_list:
        email = user.Email
        users_dict[email] = user
    return users_dict


# ユーザ登録画面：ユーザ情報登録
@app.post("/post_user")
def post_user(user: UserNew):
    new_user = UserTable(Email=user.Email,
                    age=user.age,
                    p_num=user.p_num,
                    Password=user.Password)
    session.add(new_user)
    session.commit()


# 食材登録画面：食材登録
@app.post("/post_food")
def post_food(food: FoodNew):
    new_food = FoodTable(name=food.name,
                    category=food.category,
                    price=food.price,
                    expiry_date=food.expiry_date,
                    Date=food.Date,
                    amount=food.amount,
                    unit=food.unit,
                    memo=food.memo,
                    Remaining=food.Remaining,
                    UserID=food.UserID,
                    status=food.status)
    session.add(new_food)
    session.commit()

# 食費登録画面：食費情報登録
@app.post("/post_shopping")
def post_shopping(shopping: ShoppingNew):
    new_cost = ShoppingTable(Date=shopping.Date,
                        Purpose=shopping.Purpose,
                        Price=shopping.Price,
                        UserID=shopping.UserID)
    session.add(new_cost)
    session.commit()


# 食材一覧画面：食材情報一覧取得
@app.get("/get_foods")
def get_food_list(userID: int):
    foods_list = []
    foods = session.query(FoodTable).filter(FoodTable.UserID == userID)
    for food in foods:
        tmp_food_dict = {}
        # 残日数
        remain_days = food.expiry_date - food.Date
        tmp_food_dict["Remaining_days"] = remain_days.days
        tmp_food_dict["name"] = food.name
        tmp_food_dict["category"] = food.category
        tmp_food_dict["Remaining"] = food.Remaining
        # 経過
        elapsed_days = datetime.date.today() - food.Date
        tmp_food_dict["elapsed_days"] = elapsed_days.days
        foods_list.append(tmp_food_dict)
    return foods_list


# 食材一覧画面：残量の更新
@app.put("/update_foods_remaining")
def update_foods_remaining(user: TestUser, user_id: int):
    target_user = session.query(TestUserTable).\
        filter(TestUserTable.id == user_id).first()
    target_user.name = user.name
    target_user.email = user.email
    session.commit()


# 食費一覧画面：食費情報一覧取得
@app.get("/get_shopping")
def get_shopping_list(UserID: int):
    cost_list = []
    costs = session.query(ShoppingTable).filter(ShoppingTable.UserID == UserID)
    #for cost in costs:
    #    if cost.
    return



# アラート画面：食材情報一覧取得
@app.get("/get_alert_foods")
def get_alert_food_list(userID: int):
    foods_list = []
    foods = session.query(FoodTable).filter(FoodTable.UserID == userID)
    for food in foods:
        tmp_food_dict = {}
        remain_days = food.expiry_date - food.Date
        tmp_food_dict["Remaining_days"] = remain_days.days
        tmp_food_dict["name"] = food.name
        foods_list.append(tmp_food_dict)
    # 残り日数で辞書をソート
    sorted_foods_list = sorted(foods_list, key=lambda x: x["Remaining_days"])
    return sorted_foods_list
