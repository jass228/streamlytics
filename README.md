# Streamlytics

**Streamlytics** is an [ETL](https://fr.wikipedia.org/wiki/Extract-transform-load) (Extract, Transform, Load) pipeline project designed to analyze and explore the Netflix catalogue using data from the [TMDB API](https://developer.themoviedb.org/reference/intro/getting-started).
This project aims to provide rich analytical insights into the films and series available on Netflix, such as dominant genres, average scores and production trends.

## Table of Contents

- [Streamlytics](#streamlytics)
  - [Table of Contents](#table-of-contents)
  - [Project Architecture](#project-architecture)
  - [Tech Stack](#tech-stack)
    - [Backend \& ETL](#backend--etl)
    - [Frontend](#frontend)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [API](#api)
    - [ETL](#etl)
    - [Frontend](#frontend-1)
  - [Usage](#usage)
    - [1. Run the ETL Pipeline](#1-run-the-etl-pipeline)
    - [2. Generate Statistics](#2-generate-statistics)
    - [3. Start the API](#3-start-the-api)
    - [4. Start the Frontend](#4-start-the-frontend)
  - [Project Structure](#project-structure)
  - [Demo](#demo)
  - [License](#license)
  - [Contact \& Support](#contact--support)

## Project Architecture

![Architecture Diagram](./asset/img/streamlytics_architecture.png)

1. **ETL with Airflow**: Extracts data from the TMDB API, processes it, and stores it in PostgreSQL & MongoDB.
2. **Databases**:
   - Supabase (PostgreSQL): Stores processed analytical data and statistics.
   - MongoDB: Holds raw JSON data for flexibility.
3. **FastAPI Backend**: Provides RESTful API endpoints for data access.
4. **Next.js Frontend**: Displays interactive visualizations and dashboards.
5. **Statistical Analysis**: Generates statistics and stores them in Supabase for API consumption.

## Tech Stack

### Backend & ETL

- ETL: [Apache Airflow](https://airflow.apache.org) 3.0+
- API: [FastAPI](https://fastapi.tiangolo.com)
- Databases: [Supabase](https://supabase.com) (PostgreSQL), MongoDB 8.0+
- Python 3.12+

### Frontend

- Next.js
- TailwindCSS
- Chart.js
- Nivo

## Installation

### Prerequisites

- Python >= 3.12
- MongoDB >= 8.0
- Node >= 18
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Supabase account
- TMDB API account ([get API key](https://developer.themoviedb.org/))

### API

```bash
cd api
uv init
uv sync
cp env.example .env  # Add your credentials
```

### ETL

```bash
cd etl
uv init
uv sync
cp env.example .env  # Add your credentials
```

### Frontend

```bash
cd frontend
npm install
```

## Usage

### 1. Run the ETL Pipeline

If you don't have Airflow installed, follow the [official installation guide](https://airflow.apache.org/docs/apache-airflow/stable/start.html).

```bash
# Set your Airflow home directory
export AIRFLOW_HOME=/path/to/your/airflow

# Set the DAGs folder path
export AIRFLOW__CORE__DAGS_FOLDER=/path/to/streamlytics/etl/airflow/dags

# Start Airflow
airflow standalone

# Access Airflow UI at http://localhost:8080
# Activate and run the etl_tmdb_netflix DAG
```

### 2. Generate Statistics

```bash
cd etl/stats
python main.py
```

This will:

- Extract data from PostgreSQL
- Generate statistical distributions and ratings
- Save results to Supabase `stats` table

### 3. Start the API

```bash
cd api
uvicorn main:app --reload
```

- API Documentation: http://127.0.0.1:8000/docs

### 4. Start the Frontend

```bash
cd frontend
npm run dev
```

- Visit: http://localhost:3000

## Project Structure

```plaintext
streamlytics/
├── api/                          # FastAPI Backend
│   ├── config/                   # Database configuration
│   ├── routers/                  # API routes
│   ├── services/                 # Business logic
│   └── main.py                   # Application entry point
├── etl/                          # ETL Pipeline
│   ├── airflow/                  # Airflow DAGs
│   │   └── dags/
│   │       └── netflix/          # TMDB extractors & loaders
│   └── stats/                    # Statistical analysis
│       └── utils/                # Data processing utilities
├── frontend/                     # Next.js Frontend
│   ├── components/               # React components
│   └── pages/                    # Next.js pages
└── README.md
```

## Demo

![Demo Screenshot](./asset/img/demo.jpg)

![Demo GIF](./asset/gif/demo.gif)

## License

This project is licensed under the [MIT License](LICENSE).

## Contact & Support

Author: Joseph A.  
Feel free to open an issue for questions or suggestions!
