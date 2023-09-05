# Team-5

## frontend
1. cd frontend
2. npm install
3. npm start

## backend
1. cd backend
2. pip install -r requirement.txt
3. uvicorn back:app --reload

## Dockerの使用・MySQLの確認

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

4. データベース接続
```
mysql -u root -p
```

5. どんなデータベースがあるか
```
show databases;
```

6. 使用したいデータベース(sample_db)に切り替え
```
use　sample_db;
```

7. テーブル一覧
```
show tables;
```

8. テーブル(test_user)の構造確認
```
describe test_user;
```

9. テーブル(test_user)の中身確認 
```
select * from test_user;
```

## 参考
- FastAPI + MySQL + Dockerを利用したAPI開発方法
    https://qiita.com/KWS_0901/items/684ac71e728575b6eab0

- コンテナ内のデータベース閲覧
    https://qiita.com/go_glzgo/items/3520818659a07bd17839