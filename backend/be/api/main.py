from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import session
from model import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, date, timedelta
from functions.login import *
from functions.get_users import *
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from functions.check_user import get_current_user
from sqlalchemy import func


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 許可するオリジンのリスト
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ユーザ登録画面: ユーザ情報登録
@app.post("/create_user")
async def create_user(user: User):
    try:
        actual_db_item = \
        UserTable(Password=get_password_hash(user.password),\
                   p_num=user.household,\
                      age=user.age, Email=user.email)
        session.add(actual_db_item)
        session.commit()
        
        # tokenの期限を設定
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        # tokenの作成
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
            )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Something wrong with user data",
            headers={"WWW-Authenticate": "Bearer"},
        )
        


    return {"message": "User created successfully!"}

# async def return_map_values():
#     get => food_db;

#     # 計算式


    return {"token": access_token,  "token_type": "bearer"}

# ログイン画面：　ログイン
@app.post("/token", response_model=Token)
# TODO: form_data => json from frontend input
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
async def login_for_access_token(form_data: Login):
# async def login_for_access_token(user: Login):
    print("login_for_access_token api message")
    print("TODO: change form_data to json from frontend input")
    # Get users from mysql db:
    try:
        users_db = get_users_dict()
    except Exception as e:
        print("This is post /token error")
        print("Login api error")
        print(e)
    user = authenticate_user(users_db, form_data.email, form_data.password)
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
        # TODO: make user type to User Table
        # user["user"] => user.Email
        data={"sub": user["Email"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# ホーム画面: foodデータを取得
@app.get("/food_db")
async def get_food_db(current_user: loginUser = Depends(get_current_user)):
    foods_dict = {}
    # UserIdが一致する食材を取得
    try:
        foods_lists = session.query(FoodTable).filter(FoodTable.UserID == current_user.UserID)
        for food in foods_lists:
            foodId = food.FoodID
            foods_dict[foodId] = food.toDict()
    except Exception as e:
        print("This is post /food_db error")
        print(e)
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Can't get food data from db",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return foods_dict


# アラート画面：食材情報一覧取得
@app.get("/get_alert_foods")
async def get_alert_food_list(current_user: loginUser = Depends(get_current_user)):
    foods_list = []
    foods = session.query(FoodTable).filter(FoodTable.UserID == current_user.UserID)
    for food in foods:
        tmp_food_dict = {}
        remain_days = food.expiry_date - date.today()
        if remain_days.days <= -1:
            tmp_food_dict["Remaining_days"] = "期限切れ"
        elif remain_days.days == 0:
            tmp_food_dict["Remaining_days"] = "今日中"
        else:
            tmp_food_dict["Remaining_days"] = "後" + str(remain_days.days) + "日"
        tmp_food_dict["name"] = food.name
        foods_list.append(tmp_food_dict)
    # 残り日数で辞書をソート
    sorted_foods_list = sorted(foods_list, key=lambda x: x["Remaining_days"])
    return sorted_foods_list


# 食材登録画面：食材登録
@app.post("/food_db")
async def add_food(food: FoodPost, current_user: loginUser = Depends(get_current_user)):
    try:
        new_food = FoodTable(name=food.name,
                        category=food.category,
                        price=food.price,
                        expiry_date=food.expiry_date,
                        Date=food.Date,
                        amount=food.amount,
                        unit=food.unit,
                        memo=food.memo,
                        Remaining=food.Remaining,
                        UserID=current_user.UserID,
                        status=food.status)
        session.add(new_food)
        session.commit()
    except Exception as e:
        print("This is post /post_food error")
        print(e)
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Can't post food data to db",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Food created successfully!"}

# 食材編集画面：食材編集
@app.put("/food_db")
async def fix_food(food: FoodPost, foodID: int, current_user: loginUser = Depends(get_current_user)):
    try:
        foods_lists = session.query(FoodTable).filter(FoodTable.UserID == current_user.UserID).\
            filter(FoodTable.FoodID == foodID).first()
        foods_lists.name = food.name
        foods_lists.category = food.category
        foods_lists.price = food.price
        foods_lists.expiry_date = food.expiry_date
        foods_lists.Date = food.Date
        foods_lists.amount = food.amount
        foods_lists.unit = food.unit
        foods_lists.memo = food.memo
        foods_lists.Remaining = food.Remaining
        foods_lists.status = food.status
        session.commit()
    except Exception as e:
        print("This is post /post_food error")
        print(e)
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Can't post food data to db",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Food created successfully!"}

# 食費登録画面(フード&外食)：食費情報登録
@app.post("/shopping")
async def add_shopping(shopping: ShoppingPost, current_user: loginUser = Depends(get_current_user)):
    try:
        new_cost = ShoppingTable(Date=shopping.Date,
                            Purpose=shopping.Purpose,
                            Price=shopping.Price,
                            UserID=current_user.UserID)
        session.add(new_cost)
        session.commit()

    except Exception as e:
        print("This is post /post_food error")
        print(e)
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Can't post shopping data to db",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "shopping created successfully!"}


# 食費一覧画面：食費取得
@app.get("/shopping_by_day")
async def get_cost_day(current_user: loginUser = Depends(get_current_user)):
    try:
        shopping_list = []
        #shopping_all_dict = {}
        total_cost = 0
        shopping_costs = session.query(
            ShoppingTable.Date, 
            func.sum(ShoppingTable.Price).label("TotalShoppingPrice")).\
            filter(ShoppingTable.UserID == current_user.UserID).\
                group_by(ShoppingTable.Date)
        food_costs = session.query(
            FoodTable.Date, 
            func.sum(FoodTable.price).label("TotalFoodPrice")).\
            filter(FoodTable.UserID == current_user.UserID).\
                group_by(FoodTable.Date)
        this_month = str(date.today())[:7]

        for i in range(1, 31):
            year = int(this_month[:4])
            month = int(this_month[5:7])
            tmp_date = date(year, month, i)
            tmp_dict = {}

            for shop_dict in shopping_costs:
                if tmp_date == shop_dict["Date"]:
                    tmp_dict["date"] = tmp_date
                    tmp_dict["shopping"] = shop_dict["TotalShoppingPrice"]
            for food_dict in food_costs:
                if tmp_date == food_dict["Date"]:
                    if tmp_dict != {}:
                        tmp_dict["eatout"] = food_dict["TotalFoodPrice"]
                    else:
                        tmp_dict["date"] = tmp_date
                        tmp_dict["eatout"] = food_dict["TotalFoodPrice"]

            if "date" in tmp_dict.keys():
                sum = 0
                if "shopping" in tmp_dict.keys():
                    sum += tmp_dict["shopping"]
                else:
                    tmp_dict["shopping"] = 0
                if "eatout" in tmp_dict.keys():
                    sum += tmp_dict["eatout"]
                else:
                    tmp_dict["eatout"] = 0
                tmp_dict["sum"] = sum
                total_cost += sum
                shopping_list.append(tmp_dict)
        shopping_list.insert(0, total_cost)
    except Exception as e:
        print("This is post /post_food error")
        print(e)
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Can't post shopping data to db",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return shopping_list


# 食材一覧画面：食材情報一覧取得
@app.get("/foods_info")
async def get_food_db_info(current_user: loginUser = Depends(get_current_user)):
    foods_list = []
    # UserIdが一致する食材を取得
    try:
        foods_lists = session.query(FoodTable).filter(FoodTable.UserID == current_user.UserID)
        for food in foods_lists:
            if food.status == 0:
                continue
            tmp_food_dict = {}
            # 残日数
            remain_days = food.expiry_date - date.today()
            if remain_days.days <= -1:
                tmp_food_dict["Remaining_days"] = "期限切れ"
            elif remain_days.days == 0:
                tmp_food_dict["Remaining_days"] = "今日中"
            else:
                tmp_food_dict["Remaining_days"] = "後" + str(remain_days.days) + "日"
            tmp_food_dict["name"] = food.name
            tmp_food_dict["category"] = food.category
            tmp_food_dict["Remaining"] = food.Remaining
            # 経過
            elapsed_days = date.today() - food.Date
            tmp_food_dict["Elapsed_days"] = str(elapsed_days.days) + "日"
            foods_list.append(tmp_food_dict)
    except Exception as e:
        print("This is post /food_db error")
        print(e)
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Can't get food data from db",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return foods_list



# ホーム画面: グラフデータを取得
@app.get("/graph_data")
async def get_graph_data(current_user: loginUser = Depends(get_current_user)):
    try:
        all_info_list = []
        total_cost = 0
        total_cost_list = []
        total_cost_dict = {}
        total_remain_cost_dict = {}
        total_remain_cost_list = []
        total_foodloss_cost_dict = {}
        total_foodloss_cost_list = []
        category_list = ["その他", "野菜", "肉", "魚", "穀物", "調味料", "加工食品", "飲料水"]

        shopping_costs = session.query(
            ShoppingTable.Date, 
            func.sum(ShoppingTable.Price).label("TotalShoppingPrice")).\
            filter(ShoppingTable.UserID == current_user.UserID).\
                group_by(ShoppingTable.Date)
        food_lists = session.query(FoodTable).filter(FoodTable.UserID == current_user.UserID)
        this_month = str(date.today())[:7]

        # 支出グラフ
        # 外食費の合計
        total_eatout_cost = 0
        for shop_dict in shopping_costs:
            if this_month == str(shop_dict["Date"])[:7]:
                total_eatout_cost += shop_dict["TotalShoppingPrice"]
        tmp_dict = {}
        tmp_dict["category"] = "外食"
        tmp_dict["cost"] = total_eatout_cost
        total_cost_list.append(tmp_dict)
        total_cost += total_eatout_cost
        # 食費の合計
        for food in food_lists:
            if this_month == str(food.Date)[:7]:
                category = food.category
                if category in total_cost_dict.keys():
                    total_cost_dict[category] += food.price
                else:
                    total_cost_dict[category] = food.price
        for k, v in total_cost_dict.items():
            tmp_dict = {}
            tmp_dict["category"] = category_list[k]
            tmp_dict["cost"] = v
            total_cost += v
            total_cost_list.append(tmp_dict)
        
        # 残量率
        # カテゴリーごとの残量金額の算出
        for food in food_lists:
            if food.status == 1:
                category = food.category
                price = food.price
                remain_rate = food.Remaining
                remain_price = int(price * remain_rate / 100)
                if category in total_remain_cost_dict.keys():
                    total_remain_cost_dict[category] += remain_price
                else:
                    total_remain_cost_dict[category] = remain_price
        # 残量率の算出
        total_remain_cost = 0
        for k, v in total_remain_cost_dict.items():
            total_remain_cost += v
        for k, v in total_remain_cost_dict.items():
            tmp_dict = {}
            tmp_dict["category"] = category_list[k]
            remain_rate = int(v*100/total_remain_cost)
            tmp_dict["remain_rate"] = remain_rate
            total_remain_cost_list.append(tmp_dict)


        # フードロス率
        for food in food_lists:
            if this_month == str(food.expiry_date)[:7]:
                category = food.category
                price = food.price
                remain_rate = food.Remaining
                status = food.status
                if status == 0 and remain_rate != 0:
                    loss_cost = price * remain_rate
                    if category in total_foodloss_cost_dict.keys():
                        total_foodloss_cost_dict[category] += loss_cost
                    else:
                        total_foodloss_cost_dict[category] = loss_cost
        total_foodloss_cost = 0
        for k, v in total_foodloss_cost_dict.items():
            total_foodloss_cost += v
        for k, v in total_foodloss_cost_dict.items():
            tmp_dict = {}
            tmp_dict["category"] = category_list[k]
            foodloss_rate = int(v*100/total_foodloss_cost)
            tmp_dict["foodloss_rate"] = foodloss_rate
            total_foodloss_cost_list.append(tmp_dict)

        tmp_dict = {}
        tmp_dict["monthly_cost"] = total_cost
        all_info_list.append(tmp_dict)
        tmp_dict = {}
        tmp_dict["monthly_foodloss"] = total_foodloss_cost
        all_info_list.append(tmp_dict)
        tmp_dict = {}
        tmp_dict["cost_graph"] = total_cost_list
        all_info_list.append(tmp_dict)
        tmp_dict = {}
        tmp_dict["remain_graph"] = total_remain_cost_list
        all_info_list.append(tmp_dict)
        tmp_dict = {}
        tmp_dict["foodloss_graph"] = total_foodloss_cost_list
        all_info_list.append(tmp_dict)
    except Exception as e:
        print("This is post /post_food error")
        print(e)
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Can't post shopping data to db",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return all_info_list


# # 食材一覧画面：食材情報一覧取得
# @app.get("/get_foods")
# def get_food_list(userID: int):
#     foods_list = []
#     foods = session.query(FoodTable).filter(FoodTable.UserID == userID)
#     for food in foods:
#         tmp_food_dict = {}
#         # 残日数
#         remain_days = food.expiry_date - food.Date
#         tmp_food_dict["Remaining_days"] = remain_days.days
#         tmp_food_dict["name"] = food.name
#         tmp_food_dict["category"] = food.category
#         tmp_food_dict["Remaining"] = food.Remaining
#         # 経過
#         elapsed_days = datetime.date.today() - food.Date
#         tmp_food_dict["elapsed_days"] = elapsed_days.days
#         foods_list.append(tmp_food_dict)
#     return foods_list




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

# @app.post("/eatout_register")
# async def add_data(data: EatoutData):
#     # 文字列をdatetime.dateに変換
#     converted_date = datetime.datetime.strptime(data.date, "%Y-%m-%d").date()
#     actual_db_item = Shopping(UserID=1, Date=converted_date, Price=data.price, Purpose=data.purpose)
#     session.add(actual_db_item)
#     session.commit()

#     return {"message": "Data added successfully!"}
    
    



# #　ログイン画面：ユーザー情報一覧取得
# @app.get("/get_users_dict")
# def get_users_dict():
#     users_dict = {}
#     users_list = session.query(UserTable).all()
#     for user in users_list:
#         email = user.Email
#         users_dict[email] = user
#     return users_dict




