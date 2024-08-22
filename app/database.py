from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import Config


SQLALCHEMY_DATABASE_URL = f"postgresql://{Config.settings.database_username}:{Config.settings.database_password}@{Config.settings.database_hostname}:{Config.settings.database_port}/{Config.settings.database_name}"



engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()