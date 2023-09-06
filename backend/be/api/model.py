from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from db import Base
from db import ENGINE

# テーブル定義
class TestUserTable(Base):
    __tablename__ = 'test_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    email = Column(String(128), nullable=False)

# モデル定義 
class TestUser(BaseModel):
    id: int
    name: str
    email: str

# ユーザーテーブル定義
class UserTable(Base):
    __tablename__ = 'user'
    # autoincrement：追加される毎に連番が割り振られる
    userID = Column("userID", Integer, primary_key=True, autoincrement=True)
    email = Column("email", String(128), nullable=False, unique=True)
    age = Column("age", Integer, nullable=True)
    household = Column("household", Integer, nullable=True)
    password = Column("password", String(128), nullable=False)

# ユーザーモデル定義 
class User(BaseModel):
    userID: int
    email: str
    age: int
    household: int
    password: str

def main():
    # テーブル構築
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()

