import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from . import schemas
from .schemas.base import BaseModel
from loader import config

engine = sa.create_engine(config.database_string, echo=False)
Session = sessionmaker(bind=engine)

BaseModel.metadata.create_all(engine)
