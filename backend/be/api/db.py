from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import pymysql
pymysql.install_as_MySQLdb()

# 500=>server error, url error, database error
# 400=>request error, client error, parameter error, not authorized
# 200=>success, ok
host = "127.0.0.1:3308"
db_name = "sample_db"
user = "mysqluser"
password = "mysqlpass"

DATABASE = 'mysql://%s:%s@%s/%s?charset=utf8' % (
    user,
    password,
    host,
    db_name,
)

ENGINE = create_engine(
    DATABASE,
    echo=True
)

session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)

Base = declarative_base()
Base.query = session.query_property()

