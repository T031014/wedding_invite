# 之後如用 SQLite 可放 create_engine、Session 連線設定
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 修改這邊填上你的 MySQL 資料庫資訊
DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/wedding_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
