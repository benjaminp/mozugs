from sqlalchemy import CHAR, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from util import ChoiceType

ModelBase = declarative_base()


class User(ModelBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return "<User(%s)>" % self.name


class AuthSession(ModelBase):
    __tablename__ = "auth_sessions"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user = relationship(User)
    key = Column(CHAR(32), index=True)
    expires = Column(DateTime)

    def __init__(self, user, key, expires):
        self.user = user
        self.key = key
        self.expires = expires


class Bug(ModelBase):
    __tablename__ = "bugs"

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=func.now())
    reporter_id = Column(Integer, ForeignKey("users.id"))
    reporter = relationship(User)
    title = Column(String)
    description = Column(String)
    severity = Column(ChoiceType((("m", "Minor"), ("N", "Normal"), ("M", "Major"))))
    keywords = Column(String)
    product = Column(String)
    version = Column(String)
    comments = relationship("Comment")


class Comment(ModelBase):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    bug_id = Column(Integer, ForeignKey("bugs.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(User)
    message = Column(String)
    kind = Column(ChoiceType((("d", "Description"), ("c", "Cause"), ("s", "Solution"))))
