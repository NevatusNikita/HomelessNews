from sqlalchemy import orm
from .db_session import SqlAlchemyBase
import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    salary = sqlalchemy.Column(sqlalchemy.Integer)
    place = sqlalchemy.Column(sqlalchemy.String, nullable=True)
