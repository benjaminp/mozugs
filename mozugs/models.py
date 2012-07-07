from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

ModelBase = declarative_base()


class Bug(ModelBase):
    __tablename__ = "bugs"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
