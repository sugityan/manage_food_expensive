from fastapi import FastAPI
from db import session
from model import UserTable, User, CostTable, Cost, FoodTable, Food

app = FastAPI()

#　ユーザー情報一覧取得
@app.get("/test_users")
def get_user_list():
    users = session.query(UserTable).all()
    return users


# ユーザー登録画面：ユーザー情報取得(id指定)
@app.get("/test_users/{user_id}")
def get_user(user_id: int):
    user = session.query(UserTable).\
        filter(UserTable.userID == user_id).first()
    return user


# ユーザ情報登録
@app.post("/test_users")
def post_user(user: User):
    db_test_user = User(email=user.email,
                        age=user.age,
                        household=user.household,
                        password=user.password)
    session.add(db_test_user)
    session.commit()


# ユーザ情報更新
@app.put("/test_users/{user_id}")
def put_users(user: User, user_id: int):
    target_user = session.query(UserTable).\
        filter(UserTable.id == user_id).first()
    target_user.email = user.email
    target_user.age = user.age
    target_user.household = user.household
    target_user.password = user.password
    session.commit()




#　ログイン画面：ユーザー情報一覧取得
@app.get("/get_users_dict")
def get_users_dict():
    users_dict = {}
    users_list = session.query(UserTable).all()
    for user in users_list:
        email = user.email
        users_dict[email] = user
    return users_dict


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