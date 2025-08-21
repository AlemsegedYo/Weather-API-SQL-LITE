# tests/test_api.py
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Weather, WeatherStats
from api import create_app
from datetime import date

def setup_inmemory_db(tmp_path):
    db_file = tmp_path / 'weather.db'
    engine = create_engine(f'sqlite:///{db_file}', future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, future=True)
    with Session() as s:
        s.add(
            Weather(
                station_id='STN1',
                date=date(1985, 1, 1),          # <-- use a date object
                max_temp=10.0,
                min_temp=0.0,
                precipitation=0.5,
            )
        )
        s.add(
            WeatherStats(
                station_id='STN1',
                year=1985,
                avg_max_temp=10.0,
                avg_min_temp=0.0,
                total_precipitation=0.5,
            )
        )
        s.commit()
    return str(db_file)

def test_api_weather_list(tmp_path):
    db_path = setup_inmemory_db(tmp_path)
    app = create_app(db_path)
    client = app.test_client()
    resp = client.get('/api/weather')
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 1

def test_api_stats(tmp_path):
    db_path = setup_inmemory_db(tmp_path)
    app = create_app(db_path)
    client = app.test_client()
    resp = client.get('/api/weather/stats')
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
