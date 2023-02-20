import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from data import settings

from . import schemas
from .schemas.base import BaseModel

engine = sa.create_engine(settings.DATABASE_STRING, echo=False)
Session = sessionmaker(bind=engine)

BaseModel.metadata.create_all(engine)
