from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.schema import ForeignKey
from pydantic import BaseModel
from db import Base
from db import ENGINE

# ユーザーテーブル定義
class UserTable(Base):
    __tablename__ = 'user'
    # autoincrement：追加される毎に連番が割り振られる
    userID = Column("userID", Integer, primary_key=True, autoincrement=True)
    email = Column("email", String(128), nullable=False, unique=True)
    age = Column("age", Integer, nullable=False)
    household = Column("household", Integer, nullable=False) #
    pass_word = Column("pass_word", String(128), nullable=False)

# ユーザーモデル定義 
class User(BaseModel):
    userID: int
    email: str
    age: int
    household: int
    password: str


# コストテーブル定義
class CostTable(Base):
    __tablename__ = 'cost'
    # autoincrement：追加される毎に連番が割り振られる
    costID = Column("costID", Integer, primary_key=True, autoincrement=True)
    # 型使用可能か確認
    buy_date = Column("date", Integer, nullable=False)
    usage = Column("usage", Integer, nullable=False) #
    price = Column("price", Integer, nullable=False)
    userID = Column("userID", String(128), ForeignKey("user.userID"), nullable=False)

# コストモデル定義 
class Cost(BaseModel):
    costID: int
    buy_date: int
    usage: int
    price: int
    userID: str

# 食材テーブル定義
class FoodTable(Base):
    __tablename__ = 'food'
    # autoincrement：追加される毎に連番が割り振られる
    foodID = Column("foodID", Integer, primary_key=True, autoincrement=True)
    food_name = Column("name", String(128), nullable=False)
    category = Column("category", Integer, nullable=False) #
    price = Column("price", Integer, nullable=False)
    limit_date = Column("limit_date", Integer, nullable=False)
    buy_date = Column("buy_date", Integer, nullable=False)
    amount = Column("amount", Integer, nullable=False)
    unit = Column("unit", Integer, nullable=False) #
    memo = Column("memo", String(256), nullable=False)
    userID = Column("userID", Integer, ForeignKey("user.userID"), nullable=False)
    remain_ratio = Column("price", Integer, nullable=False) #?
    #status = Column("", Integer, nullable=False)

# モデル定義 
class Food(BaseModel):
    foodID: int
    food_name: str
    category: int
    price: int
    limit_date: int
    buy_date: int
    amount: int
    unit: int
    memo: str
    userID: int
    remain_ratio: int
    


def main():
    # テーブル構築
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()

