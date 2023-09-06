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

