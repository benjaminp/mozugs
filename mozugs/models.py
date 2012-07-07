from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

ModelBase = declarative_base()


class User(ModelBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<User(%s)>" % self.name


class Bug(ModelBase):
    __tablename__ = "bugs"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
