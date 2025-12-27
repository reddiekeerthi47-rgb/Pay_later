from sqlalchemy import create_engine  #create engine is for giving the connections
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv
import os
from Models.models import Base
from sqlalchemy_utils import (create_database,
                              database_exists)

# import pymysql

load_dotenv()

class SessionMaker:
    def get_engine(self):
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        host = os.getenv("MYSQL_HOST")
        port = os.getenv("MYSQL_PORT")
        database = os.getenv("MYSQL_DATABASE")

        conn_str = \
            f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        if not database_exists(conn_str):
            create_database(conn_str)
        _engine = create_engine(conn_str, pool_size=50, echo=True)
        # Base.metadata.create_all(_engine)
        Base.metadata.create_all(bind=_engine) # To create tables (automatically,it creates tables)
        return _engine
    
    def get_session(self):   # database connection
        _engine = self.get_engine()
        session = sessionmaker(bind = _engine)
        return session