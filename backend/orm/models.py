from sqlalchemy import Column, Integer, String, Float, ForeignKey

from orm.db_setup import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    location = Column(String, ForeignKey('weather.location'))
    weather = Column(String)


class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    location = Column(String, unique=True)
    max_month = Column(Integer)
    min_month = Column(Integer)
    avg_month = Column(Float)
