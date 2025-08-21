# models.py
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Date, Float, Integer, PrimaryKeyConstraint

Base = declarative_base()

class Weather(Base):
    __tablename__ = "weather"
    station_id = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    max_temp = Column(Float)       # degrees Celsius
    min_temp = Column(Float)       # degrees Celsius
    precipitation = Column(Float)  # centimeters

    __table_args__ = (
        PrimaryKeyConstraint('station_id', 'date'),
    )

class WeatherStats(Base):
    __tablename__ = "weather_stats"
    station_id = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    avg_max_temp = Column(Float)
    avg_min_temp = Column(Float)
    total_precipitation = Column(Float)  # centimeters

    __table_args__ = (
        PrimaryKeyConstraint('station_id', 'year'),
    )
