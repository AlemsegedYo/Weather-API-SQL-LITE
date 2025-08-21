# api.py
import argparse
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import Base, Weather, WeatherStats

def create_app(db_path: str):
    db_url = f'sqlite:///{db_path}'
    engine = create_engine(db_url, echo=False, future=True)
    Session = sessionmaker(bind=engine, future=True)

    app = Flask(__name__)
    api = Api(app, version='1.0', title='Weather API', doc='/docs')

    weather_model = api.model('Weather', {
        'station_id': fields.String,
        'date': fields.String,
        'max_temp': fields.Float,
        'min_temp': fields.Float,
        'precipitation': fields.Float,
    })

    stats_model = api.model('WeatherStats', {
        'station_id': fields.String,
        'year': fields.Integer,
        'avg_max_temp': fields.Float,
        'avg_min_temp': fields.Float,
        'total_precipitation': fields.Float,
    })

    @api.route('/api/weather')
    class WeatherList(Resource):
        @api.doc(params={
            'station_id': 'Filter by station id (filename without extension)',
            'start_date': 'YYYY-MM-DD, inclusive',
            'end_date': 'YYYY-MM-DD, inclusive',
            'date': 'Exact date YYYY-MM-DD',
            'page': 'Page number (default 1)',
            'limit': 'Page size (default 100)'
        })
        @api.marshal_list_with(weather_model)
        def get(self):
            session = Session()
            q = select(Weather)

            station = request.args.get('station_id')
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            exact_date = request.args.get('date')

            if station:
                q = q.where(Weather.station_id == station)
            if exact_date:
                q = q.where(Weather.date == exact_date)
            else:
                if start_date:
                    q = q.where(Weather.date >= start_date)
                if end_date:
                    q = q.where(Weather.date <= end_date)

            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 100))
            offset = (page - 1) * limit

            q = q.order_by(Weather.station_id, Weather.date).offset(offset).limit(limit)
            rows = session.execute(q).scalars().all()

            out = []
            for r in rows:
                out.append({
                    'station_id': r.station_id,
                    'date': r.date.isoformat(),
                    'max_temp': r.max_temp,
                    'min_temp': r.min_temp,
                    'precipitation': r.precipitation,
                })
            return out

    @api.route('/api/weather/stats')
    class WeatherStatsList(Resource):
        @api.doc(params={
            'station_id': 'Filter by station id',
            'year': 'Filter by year',
            'start_year': 'Filter range start year',
            'end_year': 'Filter range end year',
            'page': 'Page number (default 1)',
            'limit': 'Page size (default 100)'
        })
        @api.marshal_list_with(stats_model)
        def get(self):
            session = Session()
            q = select(WeatherStats)

            station = request.args.get('station_id')
            year = request.args.get('year')
            start_year = request.args.get('start_year')
            end_year = request.args.get('end_year')

            if station:
                q = q.where(WeatherStats.station_id == station)
            if year:
                q = q.where(WeatherStats.year == int(year))
            else:
                if start_year:
                    q = q.where(WeatherStats.year >= int(start_year))
                if end_year:
                    q = q.where(WeatherStats.year <= int(end_year))

            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 100))
            offset = (page - 1) * limit

            q = q.order_by(WeatherStats.station_id, WeatherStats.year).offset(offset).limit(limit)
            rows = session.execute(q).scalars().all()

            out = []
            for r in rows:
                out.append({
                    'station_id': r.station_id,
                    'year': r.year,
                    'avg_max_temp': r.avg_max_temp,
                    'avg_min_temp': r.avg_min_temp,
                    'total_precipitation': r.total_precipitation,
                })
            return out

    return app

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--db-path', default='data/weather.db')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', default=5000, type=int)
    args = parser.parse_args()

    app = create_app(args.db_path)
    app.run(host=args.host, port=args.port, debug=True)
