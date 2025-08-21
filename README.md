# Weather Yield API

Weather Yield API is a robust Python toolkit for ingesting, storing, analyzing, and serving weather data using SQLite and a RESTful API. It demonstrates best practices in data engineering, statistical analysis, and API development, making it ideal for scalable, data-driven applications and informed decision-making based on environmental data.

---

## Coding Exercise Questions & Solutions

This repository addresses the following data engineering challenges:

1. **Data Modeling**: Designed a normalized database schema for weather data using SQLAlchemy ORM (`models.py`).
2. **Ingestion**: Implemented robust ingestion of weather data from raw text files, with duplicate checking and logging (`ingest.py`).
3. **Data Analysis**: Calculated yearly statistics (average max/min temperature, total precipitation) for each station and stored results in the database (`compute_stats.py`).
4. **REST API**: Developed a Flask REST API with endpoints `/api/weather` and `/api/weather/stats`, supporting filtering, pagination, and automatic Swagger/OpenAPI documentation (`api.py`).
5. **Testing**: Provided unit tests for API endpoints and ingestion logic (`tests/`).


---

## Features

- **Data Ingestion**: Import weather data from text files into a SQLite database.
- **Statistical Computation**: Compute yearly weather statistics (average max/min temperature, total precipitation) for each station.
- **REST API**: Query weather records and statistics via a Flask-based API with filtering and pagination.
- **Modular Scripts**: Separate scripts for ingestion, computation, and API serving.
- **Testing**: Unit tests for API endpoints and ingestion logic.

## Key Functionality

- Ingest weather data from `data/wx_data/*.txt` into `data/weather.db`.
- Compute and store yearly statistics in the database.
- Serve weather data and statistics through `/api/weather` and `/api/weather/stats` endpoints.
- Filter API results by station, date, or year.

## Requirements & Dependencies

- Python 3.8+
- Flask==2.3.2
- flask-restx==1.1.0
- SQLAlchemy==2.0.22
- pytest==7.4.2

All dependencies are listed in `requirements.txt`.

## Environment Setup

1. **Clone the repository**:
   ```sh
   git clone https://github.com/AlemsegedYo/weather-yield-sqlite.git
   cd weather-yield-sqlite
   ```

2. **(Optional) Create a virtual environment**:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### 1. Ingest Weather Data
Import weather data from text files into the SQLite database:
```sh
python ingest.py --data-dir data/wx_data --db-path data/weather.db
```

### 2. Compute Yearly Statistics
Calculate and store yearly statistics:
```sh
python compute_stats.py --db-path data/weather.db
```

### 3. Run the API Server
Start the Flask API server:
```sh
python api.py --db-path data/weather.db --host 127.0.0.1 --port 5000
```
Visit [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs) for interactive API documentation.

### 4. Run Tests
Execute unit tests:
```sh
pytest
```

## License

This project is licensed under the MIT License. See the `License` file for details.

## Data Source

The weather data and challenge description for this project were sourced from the Corteva code challenge template repository:

- [https://github.com/corteva/code-challenge-template](https://github.com/corteva/code-challenge-template)

## Contact

For questions or collaboration, please contact:

- **Name:** Yohana Alemseged
- **Email:** yohanatecle11@gmail.com
- **GitHub:** [AlemsegedYo](https://github.com/AlemsegedYo)

---
