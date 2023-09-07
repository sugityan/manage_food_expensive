from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    MetaData,
)
from pydantic import BaseModel
from db import Base
from db import ENGINE
from datetime import date


# テーブル定義
class TestUserTable(Base):
    __tablename__ = "test_user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    email = Column(String(128), nullable=False)


class TestUserTable2(Base):
    __tablename__ = "test_user2"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    nickname = Column(String(128), nullable=False)


class UserTable(Base):
    __tablename__ = "User"

    UserID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Password = Column(String(255), nullable=False)
    p_num = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    Email = Column(String(255), nullable=False)

    def toDict(self):
        return {
            "UserID": self.UserID,
            "password": self.Password,
            "household": self.p_num,
            "age": self.age,
            "email": self.Email,
        }


class ShoppingTable(Base):
    __tablename__ = "Shopping"

    ShoppingID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    Date = Column(Date)
    Purpose = Column(Integer, nullable=False)
    Price = Column(Integer, nullable=False)


class FoodTable(Base):
    __tablename__ = "Food"

    FoodID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("User.UserID"), nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    expiry_date = Column(Date, nullable=False)
    Date = Column(Date, nullable=False)
    amount = Column(Integer)
    unit = Column(String(255))
    memo = Column(String(255))
    Remaining = Column(Integer)
    status = Column(Integer, nullable=False)

    def toDict(self):
        return {
            "FoodID": self.FoodID,
            "UserID": self.UserID,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "expiry_date": self.expiry_date,
            "Date": self.Date,
            "amount": self.amount,
            "unit": self.unit,
            "memo": self.memo,
            "Remaining": self.Remaining,
            "status": self.status,
        }


# モデル定義
class User(BaseModel):
    password: str
    household: int
    age: int
    email: str


class loginUser(User):
    UserID: int


class Login(BaseModel):
    email: str
    password: str


class FoodAlertPut(BaseModel):
    FoodID: int
    remaining: int
    status: int


class Shopping(BaseModel):
    ShoppingID: int
    UserID: int
    Date: date
    Purpose: int
    Price: int


class Food(BaseModel):
    FoodID: int
    UserID: int
    name: str
    category: int
    price: int
    expiry_date: date
    Date: date
    amount: int
    unit: str
    memo: str
    Remaining: int
    status: int


class UserCreate(BaseModel):
    name: str
    email: str


class UserNew(BaseModel):
    Password: str
    p_num: int
    age: int
    Email: str


class ShoppingPost(BaseModel):
    Date: str
    Purpose: int
    Price: int


class FoodPost(BaseModel):
    name: str
    category: int
    price: int
    expiry_date: str
    Date: str
    amount: int
    unit: str
    memo: str
    Remaining: int
    status: int


class FoodPut(BaseModel):
    FoodID: int
    name: str
    category: int
    price: int
    expiry_date: str
    Date: str
    amount: int
    unit: str
    memo: str
    Remaining: int
    status: int


class FoodPatch(BaseModel):
    foodID: int
    remaining: int
    status: int


class CostByDate(BaseModel):
    Date: date
    Purpose: int
    Price: int


class EatoutData(BaseModel):
    date: str  # YYYY-MM-DD 形式の文字列
    price: int
    purpose: int


def main():
    # テーブル構築
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()
