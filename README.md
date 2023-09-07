# Team-5

## 目次
- [目次](#目次)
- [ログインアカウント](#loginaccount)
- [frontend](#frontend)
- [SwaggerUIの起動(backend)](#swaggeruiの起動backend)
- [Dockerの使用・MySQLの確認](#dockerの使用・mysqlの確認)
    - [Command一覧](#command一覧)
    - [参考](#参考)
- [設計](#設計)
    - [テーブル図](#テーブル図)
        - [Userテーブル](#userテーブル)
        - [Foodテーブル](#foodテーブル)
        - [Shoppingテーブル](#shoppingテーブル)

## LoginAccount
email: test
password: password

## frontend
1. cd frontend
2. npm install
3. npm start

## SwaggerUIの起動(backend)
1. cd backend
2. cd be
2. pip install -r requirements.txt
3. cd api
4. uvicorn main:app --reload

## docker-compose.yamlのplatform設定
platformをM1マック用に指定してありますが、M1マック以外の方はコメントアウトしてください。
[docker-compose.yml](./docker-compose.yml)
<br>
```
platform: linux/x86_64
```

## Dockerの使用・MySQLの確認
### Command一覧
1. コンテナ起動
```
docker-compose up -d --build
```

2. コンテナ(db)に入る
```
docker exec -it db bash
```

3. mysqlへ接続
```
mysql -u root -p
Enter password:　rootpass
```

4. どんなデータベースがあるか
```
show databases;
```

5. 使用したいデータベース(sample_db)に切り替え
```
use　sample_db;
```

6. テーブル一覧
```
show tables;
```

7. テーブル(test_user)の構造確認
```
describe test_user;
```

8. テーブル(test_user)の中身確認 
```
select * from test_user;
```

### 参考
- FastAPI + MySQL + Dockerを利用したAPI開発方法
    https://qiita.com/KWS_0901/items/684ac71e728575b6eab0

- コンテナ内のデータベース閲覧
    https://qiita.com/go_glzgo/items/3520818659a07bd17839

- dockerをterminalで扱う
  https://qiita.com/kooohei/items/0e788a2ce8c30f9dba53


## 設計

```mermaid
classDiagram
    User -- Shopping : 1 - n (ユーザーは多数の購買記録を持つ)
    User -- Food : 1 - n (ユーザーは多数の食べ物を持つ)

    class User {
        +UserID (PK)
        Password
        p_num
        age
        Email
    }

    class Food {
       +FoodID(PK)
       +UserID(FK)
       name
       category
       price
       expiry_date
       Date
       amount
       unit
       memo
       Remaining
       status
    }

    class Shopping {
        +ShoppingID (PK)
        +UserID (FK)
        Date
        Purpose
        Price
    }

```
---

#### Userテーブル
パスワードはバックエンド側でハッシュ化して,ハッシュ化したものを保存します。

| カラム名  | 説明       | 型 | 
|---------|-----------|---------------|
| UserID  | ユーザーID (パーティションキー) | int(11) | 
| Password | ハッシュ化したパスワード   | varchar(255) |
| p_num   | 世帯数 | int(11) |
| age     | 年齢       | int(11) |
| Email | メールアドレス | varchar(255) |

---

#### Foodテーブル

| カラム名  | 説明       | 型 |
|---------|-----------|---------------|
| FoodID  | フードID (パーティションキー) | int(11) |
| UserID | ユーザーID (フォーリンキー)  | int(11) |
| name   | フードの名前 | varchar(255) |
| category     | フードのカテゴリ       | int(11) |
| price | 値段 | int(11) |
| expiry_date | 賞味期限 | date |
| Date | 購入日 | date |
| amount | 量/個数 | int(11) |
| unit | 単位 | varchar(255) |
| memo | メモ | varchar(255) |
| Remaining | 残り(%) | int(11) |
| status | 消費したかどうかの状況(0 or 1) 0がない状態, 1がある状態| int(11) |

---
#### Shoppingテーブル

| カラム名  | 説明       | 型 |
|---------|-----------|---------------|
| ShoppingID  | フードID (パーティションキー) | int(11) |
| UserID | ユーザーID (フォーリンキー)   | int(11) |
| Date   | 購入日 | date |
| Purpose     | 目的       | int(11) |
| Price | 値段 | int(11) |

----

#### user register page関連

##### POST `/create_user`
```
// request
{
  "Password": "pass",
  "p_num": 0,
  "age": 0,
  "Email": "mail"
}
```
```
// response
{"message": "User created successfully!"}
```
----

#### login page関連

##### POST `/login`
```
// request
{
  "email": "mail",
  "password": "pass"
}
```
```
// response
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYWlsIiwiZXhwIjoxNjk0MDE5OTQyfQ.xgRHowsf4UIDni8aYNC84X6h5CWAthFYaWCHzLm0Q88",
  "token_type": "bearer"
}
```
----


#### Home page関連

##### GET `/food_db`
```
// /food_db

// レスポンスはリストになって返ってくる.
{
  "3": {
    "FoodID": 3,
    "UserID": 8,
    "name": "test",
    "category": 0,
    "price": 200,
    "expiry_date": "2023-10-10",
    "Date": "2023-10-09",
    "amount": 1,
    "unit": "0",
    "memo": "a",
    "Remaining": 1,
    "status": 1
  },
  "4": {
    "FoodID": 4,
    "UserID": 8,
    "name": "test2",
    "category": 1,
    "price": 200,
    "expiry_date": "2023-10-10",
    "Date": "2023-10-09",
    "amount": 1,
    "unit": "0",
    "memo": "a",
    "Remaining": 1,
    "status": 1
  }
}
```

----

##### GET `/get_alert_foods`
```
// /get_alert_foods'
  
// レスポンスはリストになって返ってくる.
[
  {
    "Remaining_days": 1,
    "name": "test"
  },
  {
    "Remaining_days": 1,
    "name": "test2"
  }
]
```

----
#### Food page関連

##### Post `/food_db`

```
// request
{
  "name": "test3",
  "category": 1,
  "price": 100,
  "expiry_date": "2023-09-06",
  "Date": "2023-09-06",
  "amount": 2,
  "unit": "0",
  "memo": "no",
  "Remaining": 2,
  "status": 0
}
```
```
// response
{
  "message": "Food created successfully!"
}
```

----

##### PUT `/food_db`

```
curl -X 'PUT' \
  'http://127.0.0.1:8000/food_db?foodID=3' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjk0MDI3MzA4fQ.hat9b3irYX_PaxU5SQyJ8L5rVXirehbwNAbfKkhf6GU' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "test",
  "category": 0,
  "price": 0,
  "expiry_date": "2023-09-06",
  "Date": "2023-09-06",
  "amount": 0,
  "unit": "string",
  "memo": "string",
  "Remaining": 0,
  "status": 0
}'
```

```
// request
{
  "name": "test",
  "category": 0,
  "price": 0,
  "expiry_date": "2023-09-06",
  "Date": "2023-09-06",
  "amount": 0,
  "unit": "string",
  "memo": "string",
  "Remaining": 0,
  "status": 0,
}
```
```
// response
{
  "message": "Food created successfully!"
}
```

----

##### POST `/shopping`

```
curl -X 'POST' \
  'http://127.0.0.1:8000/shopping' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjk0MDI3NjI2fQ.FmBw_NDEfhJcgc6dpv8bnGo1ZP7kpZnjCaHebfz_SAE' \
  -H 'Content-Type: application/json' \
  -d '{
  "Date": "2023-09-06",
  "Purpose": 0,
  "Price": 100
}'
```

```
// request
{
  "Date": "2023-09-06",
  "Purpose": 0,
  "Price": 100
}
```
```
{
  "message": "shopping created successfully!"
}
```
