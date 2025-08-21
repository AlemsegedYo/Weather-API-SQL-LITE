# compute_stats.py
import argparse
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Base, Weather, WeatherStats

def compute(db_path: str):
    db_url = f'sqlite:///{db_path}'
    engine = create_engine(db_url, echo=False, future=True)
    Session = sessionmaker(bind=engine, future=True)

    Base.metadata.create_all(engine)

    with Session() as session:
        # extract year using strftime for SQLite
        stmt = (
            select(
                Weather.station_id,
                func.strftime('%Y', Weather.date).label('year'),
                func.avg(Weather.max_temp).label('avg_max'),
                func.avg(Weather.min_temp).label('avg_min'),
                func.sum(Weather.precipitation).label('total_precip')
            )
            .where(Weather.date != None)
            .group_by(Weather.station_id, func.strftime('%Y', Weather.date))
        )

        results = session.execute(stmt).all()

        inserted = 0
        for row in results:
            station_id = row.station_id
            year = int(row.year)
            avg_max = float(row.avg_max) if row.avg_max is not None else None
            avg_min = float(row.avg_min) if row.avg_min is not None else None
            total_precip = float(row.total_precip) if row.total_precip is not None else None

            ws = WeatherStats(
                station_id=station_id,
                year=year,
                avg_max_temp=avg_max,
                avg_min_temp=avg_min,
                total_precipitation=total_precip,
            )
            session.merge(ws)
            inserted += 1
        session.commit()

    print(f"Stored {inserted} yearly-stat rows.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--db-path', default='data/weather.db')
    args = parser.parse_args()
    compute(args.db_path)
