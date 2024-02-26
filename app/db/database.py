from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import psycopg2
from dotenv import load_dotenv,find_dotenv
import os 

load_dotenv(find_dotenv())
BASE_DIR = Path(__file__).resolve().parent # webApp\app\db
username = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
dbname = os.getenv("POSTGRES_DBNAME")
test_dbname = os.getenv("POSTGRES_TEST_DBNAME")
SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{test_dbname}"
# SQLALCHEMY_DATABASE_URL = f"sqlite:///{BASE_DIR}/sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# engine = create_engine(SQLALCHEMY_DATABASE_URL,
                    #    connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # 工厂模式

if __name__ == "__main__":
    conn = psycopg2.connect(user=username, password=password, host=host, port=port, database=test_dbname)
    cur = conn.cursor()
    cur.execute("GRANT CREATE ON SCHEMA public TO future;")
    # cur.execute("GRANT USAGE ON SCHEMA public TO future;")
    #给future用户增删改查database postgres的权限


    # 创建模式，叫test_env
    # cur.execute("CREATE SCHEMA test_env;")
    # cur.execute("GRANT CREATE ON SCHEMA test_env TO future;")

    # 删除public模式中的表
    cur.execute("DROP SCHEMA public CASCADE;")

    # 创建public模式
    cur.execute("CREATE SCHEMA public;")
    conn.commit()
    cur.close()
    conn.close()
