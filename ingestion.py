# ingest.py
import argparse
import logging
from datetime import datetime
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Weather

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

def parse_line(line: str):
    parts = line.strip().split('\t')
    if len(parts) < 4:
        return None
    date_str, max_t, min_t, precip = parts[:4]
    # parse date
    try:
        date = datetime.strptime(date_str, '%Y%m%d').date()
    except Exception:
        return None

    def conv_int_field(val: str):
        if val == '-9999':
            return None
        try:
            return int(val)
        except Exception:
            return None

    max_t_i = conv_int_field(max_t)
    min_t_i = conv_int_field(min_t)
    precip_i = conv_int_field(precip)

    max_temp = None if max_t_i is None else (max_t_i / 10.0)
    min_temp = None if min_t_i is None else (min_t_i / 10.0)
    # precip: tenths of mm -> cm. (value / 10) -> mm, then /10 -> cm => /100
    precip_cm = None if precip_i is None else (precip_i / 100.0)

    return date, max_temp, min_temp, precip_cm

def ingest(data_dir: str, db_path: str):
    db_url = f'sqlite:///{db_path}'
    engine = create_engine(db_url, echo=False, future=True)
    Session = sessionmaker(bind=engine, future=True)

    Base.metadata.create_all(engine)

    start = datetime.utcnow()
    logger.info(f"Starting ingestion: data_dir={data_dir} db={db_path} at {start.isoformat()}Z")

    total_lines = 0
    inserted = 0
    skipped = 0

    with Session() as session:
        for fname in sorted(os.listdir(data_dir)):
            fpath = os.path.join(data_dir, fname)
            if not os.path.isfile(fpath):
                continue
            station_id = os.path.splitext(fname)[0]
            logger.info(f"Processing station file: {fname} -> station_id={station_id}")
            with open(fpath, 'r', encoding='utf-8') as fh:
                for line in fh:
                    total_lines += 1
                    parsed = parse_line(line)
                    if parsed is None:
                        skipped += 1
                        continue
                    date, max_temp, min_temp, precip_cm = parsed
                    # Check if record exists
                    existing = session.query(Weather).filter_by(station_id=station_id, date=date).first()
                    if existing is None:
                        # Insert new record
                        w = Weather(
                            station_id=station_id,
                            date=date,
                            max_temp=max_temp,
                            min_temp=min_temp,
                            precipitation=precip_cm,
                        )
                        session.add(w)
                        inserted += 1
                    else:
                        # Only update if any value is different
                        if (
                            existing.max_temp != max_temp or
                            existing.min_temp != min_temp or
                            existing.precipitation != precip_cm
                        ):
                            existing.max_temp = max_temp
                            existing.min_temp = min_temp
                            existing.precipitation = precip_cm
                            inserted += 1
        session.commit()

    end = datetime.utcnow()
    logger.info(f"Finished ingestion at {end.isoformat()}Z. Duration: {end - start}")
    logger.info(f"Total lines read: {total_lines}, inserted/updated: {inserted}, skipped: {skipped}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', default='data/wx_data', help='Directory containing raw weather files')
    parser.add_argument('--db-path', default='data/weather.db', help='SQLite DB path')
    args = parser.parse_args()
    os.makedirs(os.path.dirname(args.db_path) or '.', exist_ok=True)
    ingest(args.data_dir, args.db_path)
