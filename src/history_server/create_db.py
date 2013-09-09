from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import get_engine, get_db_session, init_db, Base


if __name__ == '__main__':
    engine = get_engine('sqlite:///history.sql')
    init_db(engine, Base)