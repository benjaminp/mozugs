from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from util import ChoiceType

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
    severity = Column(ChoiceType((("m", "minor"), ("N", "normal"), ("M", "major"))))
    keywords = Column(String)
    product = Column(String)
    version = Column(String)


class Comment(ModelBase):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    user = Column(String) # TODO: FK
    message = Column(String)
