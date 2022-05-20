from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_engine(settings.postgres_url)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BaseModel = declarative_base()
