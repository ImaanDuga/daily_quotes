# Daily Quotes

A Flask web application that displays an inspirational quote of the day, backed by a PostgreSQL database with full CRUD support.

## Live Demo

https://web-production-84632.up.railway.app

## Features

- Quote of the day — rotates automatically based on the current date
- View all quotes in a table
- Add, edit, and delete quotes
- Auto-seeds 10 default quotes on first run
- Deployed on Railway with PostgreSQL

## Tech Stack

- Python Flask
- Flask-SQLAlchemy
- PostgreSQL
- Gunicorn
- HTML / CSS / JavaScript

## Local Setup

1. Clone the repo
```bash
git clone https://github.com/ImaanDuga/daily_quotes.git
cd daily_quotes
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the app
```bash
python app.py
```

Visit `http://localhost:5000`

## Environment Variables

| Variable       | Description                        |
|----------------|------------------------------------|
| `DATABASE_URL` | PostgreSQL connection string       |
| `SECRET_KEY`   | Flask session secret key           |

Copy `.env.example` to `.env` and fill in your values for local Postgres. Without `DATABASE_URL`, the app defaults to SQLite.

## Routes

| Route                   | Method     | Description              |
|-------------------------|------------|--------------------------|
| `/`                     | GET        | Quote of the day         |
| `/quotes`               | GET        | All quotes               |
| `/quotes/add`           | GET / POST | Add a new quote          |
| `/quotes/edit/<id>`     | GET / POST | Edit an existing quote   |
| `/quotes/delete/<id>`   | POST       | Delete a quote           |
| `/health`               | GET        | Health check             |

## Deployment

The app is deployed on Railway. Every push to the `main` branch triggers an automatic redeploy via Railway's GitHub integration.
