import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from . import schemas

from .schemas.base import BaseModel

engine = sa.create_engine("postgresql+psycopg2://xqmuqvvbsbyseu:86341b10a67c27d0bef4d5b06a02fabf36ad2d89869e1fdbafe284082db21d9f@ec2-54-74-35-87.eu-west-1.compute.amazonaws.com:5432/dec42iv68d9chg", echo=False)
Session = sessionmaker(bind=engine)

BaseModel.metadata.create_all(engine)

