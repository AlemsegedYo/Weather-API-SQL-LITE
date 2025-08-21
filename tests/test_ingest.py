# tests/test_ingest.py
import os
import tempfile
from ingest import parse_line, ingest
from models import Base, Weather
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def test_parse_line_valid():
    line = '19850101\t100\t-50\t25\n'
    parsed = parse_line(line)
    assert parsed is not None
    date, max_t, min_t, precip = parsed
    assert max_t == 10.0
    assert min_t == -5.0
    assert abs(precip - 0.25) < 1e-9

def test_ingest_creates_db(tmp_path):
    # create temporary data dir
    d = tmp_path / "wx_data"
    d.mkdir()
    f = d / "STN1.txt"
    f.write_text('19850101\t100\t-50\t25\n')

    db_file = tmp_path / "weather.db"
    ingest(str(d), str(db_file))

    engine = create_engine(f'sqlite:///{db_file}', future=True)
    Session = sessionmaker(bind=engine, future=True)
    Base.metadata.create_all(engine)
    with Session() as s:
        rows = s.query(Weather).all()
        assert len(rows) == 1
        r = rows[0]
        assert r.station_id == 'STN1'
        assert r.max_temp == 10.0
