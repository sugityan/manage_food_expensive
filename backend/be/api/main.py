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
from sqlalchemy import case


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
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Something wrong with user data",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # tokenの期限を設定
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # tokenの作成
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
        )
    return {"access_token": access_token, "token_type": "bearer"}

# ログイン画面：　ログイン
@app.post("/login", response_model=Token)
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
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# swaggerUI: tokenの確認
@app.post("/token", response_model=Token)
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
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


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
        if food.status == 0:
            continue
        else:
            tmp_food_dict = {}
            remain_days = food.expiry_date - date.today()
            if remain_days.days <= -1:
                tmp_food_dict["Remaining_days"] = "期限切れ"
            elif remain_days.days == 0:
                tmp_food_dict["Remaining_days"] = "今日中"
            else:
                tmp_food_dict["Remaining_days"] = "後" + str(remain_days.days) + "日"
            tmp_food_dict["name"] = food.name
            tmp_food_dict["foodID"] = food.FoodID
            tmp_food_dict["Remaining"] = food.Remaining
            foods_list.append(tmp_food_dict)
    # 残り日数で辞書をソート
    sorted_foods_list = sorted(foods_list, key=lambda x: x["Remaining_days"], reverse=True)
    return sorted_foods_list

# 食材編集画面：食材編集
@app.put("/food_db/{FoodID}")
# @app.put("/food_db_new")
async def update_remaining(FoodID: int, remaining: int, status: int, current_user: loginUser = Depends(get_current_user)):
    print("0000")
    try:
        # foodidで既存の食品レコードを検索
        food_item = session.query(FoodTable).filter(FoodTable.FoodID == FoodID).first()
        
        if not food_item:
            raise HTTPException(status_code=404, detail="Food not found")

        # Remaining フィールドを更新
        food_item.Remaining = remaining
        food_item.status = status

        # 変更をデータベースにコミット
        session.commit()
    except Exception as e:
        print("This is put /food_db/{foodid} error")
        print(e)
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Can't update remaining food data to db",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Food remaining updated successfully!"}
###########################################################

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
        new_cost = ShoppingTable(
            Date=shopping.Date,
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
        costs = session.query(
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
        all_info_dict = {}
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
            tmp_dict["cost"] = remain_rate
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
            tmp_dict["cost"] = foodloss_rate
            total_foodloss_cost_list.append(tmp_dict)

        all_info_dict["monthly_cost"] = total_cost
        all_info_dict["monthly_foodloss"] = total_foodloss_cost
        all_info_dict["cost_graph"] = total_cost_list
        all_info_dict["remain_graph"] = total_remain_cost_list
        all_info_dict["foodloss_graph"] = total_foodloss_cost_list

    except Exception as e:
        print("This is post /post_food error")
        print(e)
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Can't post shopping data to db",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return all_info_dict



# 門倉編集分
@app.get("/compare_cost")
def get_food_db_info(current_user: loginUser = Depends(get_current_user)):

    user_age = current_user.age

    today = date.today()
    one_month_ago = today - timedelta(days=30)

    # その人の食費計算

    foodcost_result = session.query(func.sum(ShoppingTable.Price).label("totalcost")).filter(
        ShoppingTable.UserID == current_user.UserID,
        ShoppingTable.Date.between(one_month_ago, today)  
    ).group_by(
        ShoppingTable.UserID
    ).first()

    if foodcost_result:
        foodcost = foodcost_result.totalcost
    else:
        foodcost = 0

    foodcostRanking = "10万円~"
    if foodcost < 30000:
        foodcostRanking = "~3万円"
    elif foodcost >= 30000 and foodcost < 40000:
        foodcostRanking = "3万円~4万円"
    elif foodcost >= 40000 and foodcost < 50000:
        foodcostRanking = "3万円~4万円"
    elif foodcost >= 50000 and foodcost < 60000:
        foodcostRanking = "3万円~4万円"
    elif foodcost >= 60000 and foodcost < 80000:
        foodcostRanking = "3万円~4万円"
    elif foodcost >= 80000 and foodcost < 100000:
        foodcostRanking = "3万円~4万円"
    else:
        foodcostRanking = "10万円~"


    # その人のフードロス計算
    foodloss_result = session.query(FoodTable.UserID, func.sum(FoodTable.price).label("totalloss")).filter(
        FoodTable.UserID == current_user.UserID,
        FoodTable.expiry_date.between(one_month_ago, today), 
        FoodTable.status == 0,
        FoodTable.Remaining != 0
    ).group_by(
        FoodTable.UserID
    ).first()

    if foodloss_result:
        foodloss = foodloss_result.totalloss
    else:
        foodloss = 0

    foodlossPosition = "1万円~"
    if foodloss < 1000:
        foodlossPosition = "~千円"
    elif foodloss >= 1000 and foodcost < 2000:
        foodlossPosition = "千円~2千円"
    elif foodloss >= 2000 and foodcost < 2000:
        foodlossPosition = "2千円~3千円"
    elif foodloss >= 3000 and foodcost < 5000:
        foodlossPosition = "3千円~5千円"
    elif foodloss >= 5000 and foodcost < 7000:
        foodlossPosition = "5千円~7千円"
    elif foodloss >= 7000 and foodcost < 10000:
        foodlossPosition = "7千円~1万円"
    else:
        foodlossPosition = "1万円~"



    # その人の年代はどこですか？
    if user_age <= 29:
        min_age = 0
        max_age = 29
    elif user_age >=30 and user_age <=39:
        min_age = 30
        max_age = 39
    elif user_age >= 40 and user_age <= 49:
        min_age = 40
        max_age = 49
    else :
        min_age = 50
        max_age = 10000

    # 同年代のユーザーIDを集める
    gen = session.query(UserTable.UserID).filter(UserTable.age.between(min_age, max_age)).subquery()
    
    # 食費のグラフ用に分類
    b = session.query(gen.c.UserID, func.sum(ShoppingTable.Price).label("total")).join(
        ShoppingTable, gen.c.UserID == ShoppingTable.UserID
    ).filter(
        ShoppingTable.Date.between(one_month_ago, today)  # dateカラムの値が1ヶ月前と今日の間であることを確認
    ).group_by(
        gen.c.UserID
    ).subquery()
    
    record = session.query(
        case(
            (b.c.total < 30000, "~3万円"),
            ((b.c.total >= 30000) & (b.c.total < 40000), "3万円~4万円"),
            ((b.c.total >= 40000) & (b.c.total < 50000), "4万円~5万円"),
            ((b.c.total >= 50000) & (b.c.total < 60000), "5万円~6万円"),
            ((b.c.total >= 60000) & (b.c.total < 80000), "6万円~8万円"),
            ((b.c.total >= 80000) & (b.c.total < 100000), "8万円~10万円"),
            else_="10万円~"
        ).label("name"),
        func.count().label("number")
    ).group_by("name").all()

    record_dict = {item[0]: item[1] for item in record}

    price_ranges = [
    "~3万円",
    "3万円~4万円",
    "4万円~5万円",
    "5万円~6万円",
    "6万円~8万円",
    "8万円~10万円",
    "10万円~"
    ]

    foodcostData = [
        {
            "name": price_range,
            "number": record_dict.get(price_range, 0)  # 辞書から価格範囲の数を取得、存在しない場合は0を使用。
        } 
        for price_range in price_ranges
    ]

    # フードロスのグラフように分類
    a = session.query(gen.c.UserID, func.sum(FoodTable.price).label("total")).join(
        FoodTable, gen.c.UserID == FoodTable.UserID
    ).filter(
        FoodTable.expiry_date.between(one_month_ago, today), 
        FoodTable.status == 0,
        FoodTable.Remaining != 0
    ).group_by(
        gen.c.UserID
    ).subquery()


    record = session.query(
        case(
            (b.c.total < 1000, "~千円"),
            ((b.c.total >= 1000) & (b.c.total < 2000), "千円~2千円"),
            ((b.c.total >= 2000) & (b.c.total < 3000), "2千円~3千円"),
            ((b.c.total >= 3000) & (b.c.total < 5000), "3千円~5千円"),
            ((b.c.total >= 5000) & (b.c.total < 7000), "5千円~7千円"),
            ((b.c.total >= 7000) & (b.c.total < 10000), "7千円~1万円"),
            else_="1万円~"
        ).label("name"),
        func.count().label("number")
    ).group_by("name").all()

    loss_ranges = [
        "~千円",
        "千円~2千円",
        "2千円~3千円",
        "3千円~5千円",
        "5千円~7千円",
        "7千円~1万円",
        "1万円~"
    ]

    # 最終結果のリストを作成します。
    foodlossData = [
        {
            "name": loss_range,
            "number": record_dict.get(loss_range, 0)  # 辞書から価格範囲の数を取得、存在しない場合は0を使用。
        } 
        for loss_range in loss_ranges
    ]

    result = {
        "foodcostRanking" : foodcostRanking,
        "foodcost" :foodcost,
        "foodcostData" : foodcostData,
        "foodlossPosition" : foodlossPosition,
        "foodloss" : foodloss,
        "foodlossData" : foodlossData
    }

    return result

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




