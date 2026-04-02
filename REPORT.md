# PaaS Practical Assignment Report
## Deploying a Flask Web Application on Railway

**Student:** Imaan Duga  
**Date:** April 2026  
**Application URL:** https://web-production-84632.up.railway.app  
**GitHub Repository:** https://github.com/ImaanDuga/daily_quotes  

---

## 1. Deployment Process

### Application Overview
The deployed application is a Daily Quotes web app built with Python Flask. It displays an inspirational quote of the day, rotated every 10 minutes, and provides full CRUD (Create, Read, Update, Delete) functionality for managing quotes through a web interface.

### Technology Stack
- **Backend:** Python Flask with Flask-SQLAlchemy ORM
- **Database:** PostgreSQL (Railway-managed)
- **Frontend:** HTML, CSS, JavaScript (Jinja2 templating)
- **Server:** Gunicorn (production WSGI server)
- **Platform:** Railway PaaS

### Deployment Steps

**Step 1 — Application Development**  
The Flask application was developed locally with SQLite for development. The app was structured with environment variable support so it automatically switches to PostgreSQL in production via the `DATABASE_URL` environment variable injected by Railway.

**Step 2 — GitHub Repository Setup**  
The source code was pushed to a GitHub repository at `https://github.com/ImaanDuga/daily_quotes`. A `.gitignore` file was included to exclude sensitive files like `.env` and the local SQLite database.

**Step 3 — Railway Project Creation**  
A new project was created on Railway by connecting the GitHub repository. Railway automatically detected the Python application, installed dependencies from `requirements.txt`, and used the `Procfile` to start the app with Gunicorn:
```
web: gunicorn app:app
```

**Step 4 — Database Provisioning**  
A PostgreSQL database was provisioned directly from the Railway dashboard. Railway automatically injected the `DATABASE_URL` environment variable into the application's environment, enabling a seamless connection without hardcoding credentials.

**Step 5 — Environment Variables**  
The following environment variables were configured in Railway's Variables tab:
- `DATABASE_URL` — auto-injected by Railway when PostgreSQL was added
- `SECRET_KEY` — manually set for Flask session security

**Step 6 — Database Seeding**  
On first startup, the application automatically seeds the database with 10 default quotes if the table is empty, ensuring the app is functional immediately after deployment.

---

## 2. Environment & Configuration Management

Sensitive configuration is handled entirely through environment variables, following the 12-Factor App methodology. No credentials are hardcoded in the source code.

In the application:
```python
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///quotes.db")
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")
```

This pattern means:
- Locally, the app falls back to SQLite with a development secret key
- On Railway, it uses the production PostgreSQL database and a secure secret key
- The `.env.example` file documents required variables without exposing actual values
- The `.gitignore` ensures the `.env` file is never committed to version control

---

## 3. Database Integration

### Schema
The application uses a single `quote` table:

| Column      | Type         | Description                  |
|-------------|--------------|------------------------------|
| id          | Integer (PK) | Auto-incrementing primary key |
| text        | String(500)  | The quote content             |
| author      | String(100)  | The quote author              |
| created_at  | DateTime     | Timestamp of creation         |

### CRUD Operations
All four CRUD operations are implemented:

- **Create** — `POST /quotes/add` inserts a new quote into the database
- **Read** — `GET /` displays the quote of the day; `GET /quotes` lists all quotes
- **Update** — `GET/POST /quotes/edit/<id>` allows editing an existing quote
- **Delete** — `POST /quotes/delete/<id>` removes a quote from the database

### Sample Data
The database is seeded with 10 quotes on first deployment, including quotes from Steve Jobs, Albert Einstein, Winston Churchill, and others.

---

## 4. Scalability Awareness

### Railway's Usage-Based Pricing
Railway charges based on actual resource consumption (CPU and RAM) rather than fixed tiers. The free tier provides $5 of credit per month, which is sufficient for low-traffic applications.

### Impact of Increased Traffic
As traffic increases on the Daily Quotes app:
- **Database connections** would increase, potentially hitting connection pool limits
- **Memory usage** would rise as Flask handles more concurrent requests
- **Response times** could degrade under high load with a single Gunicorn worker

### Scaling Plan
1. **Vertical scaling** — Increase RAM and CPU allocation in Railway's service settings
2. **Horizontal scaling** — Railway supports multiple replicas; increase replica count to distribute load
3. **Database scaling** — Upgrade the PostgreSQL plan for higher connection limits and storage
4. **Caching** — Add Redis (available on Railway) to cache the quote of the day and reduce DB queries
5. **CDN** — Serve static assets (CSS, JS) via a CDN to reduce server load

Railway's auto-scaling based on usage means costs scale proportionally with traffic, making it cost-effective for variable workloads.

---

## 5. CI/CD Workflow

The CI/CD pipeline was implemented by connecting the GitHub repository to Railway. The workflow is:

1. Code changes are made locally
2. Changes are committed and pushed to the `main` branch on GitHub
3. Railway detects the push via a webhook
4. Railway automatically pulls the latest code, rebuilds the application, and redeploys it
5. The new version goes live with zero manual intervention

This was verified during development — when the database seeding feature was added, a `git push` triggered an automatic redeploy within approximately 60 seconds, and the changes were live immediately after.

---

## 6. Monitoring & Logging

Railway provides real-time logs accessible from the service dashboard under the "Logs" tab.

### Error Encountered
During initial deployment, the application failed to start with the following error in Railway logs:
```
sqlalchemy.exc.OperationalError: could not connect to server: Connection refused
```

### Resolution
The error occurred because the application was trying to connect to the database before Railway had fully provisioned the PostgreSQL instance. The fix involved ensuring the `DATABASE_URL` environment variable was correctly set in Railway's Variables tab and redeploying. Once the variable was confirmed, the connection succeeded and the app started normally.

Railway's logs were essential in identifying this issue — the full stack trace pointed directly to the database connection, making the fix straightforward.

---

## 7. Comparison: Railway vs Heroku

| Feature              | Railway                          | Heroku                            |
|----------------------|----------------------------------|-----------------------------------|
| Free tier            | $5/month credit                  | No free tier (removed 2022)       |
| Deployment           | Git push auto-deploy             | Git push auto-deploy              |
| Database             | Postgres, MySQL, Redis built-in  | Postgres add-on (paid)            |
| Pricing model        | Usage-based                      | Dyno-based (fixed tiers)          |
| Sleep on inactivity  | No                               | Yes (on free dynos previously)    |
| Setup complexity     | Very simple, minimal config      | Slightly more configuration       |
| Dashboard UI         | Modern, intuitive                | Mature but older UI               |
| Custom domains       | Supported                        | Supported                         |

### Reflection
Railway proved to be an excellent PaaS for this assignment. The deployment process was straightforward — connecting a GitHub repository and adding a database took under 10 minutes. The automatic injection of `DATABASE_URL` eliminated manual configuration steps that would be required on other platforms.

Compared to Heroku, Railway's usage-based pricing is more transparent and cost-effective for small projects. Heroku's removal of its free tier in 2022 makes Railway a more accessible alternative for students and developers building small applications.

The main challenge encountered was the initial database connection error, which was quickly resolved using Railway's logging tools. Overall, Railway provides a smooth developer experience with minimal infrastructure overhead, allowing focus on application development rather than server management.

---

## Deliverables Summary

- **Deployed URL:** https://web-production-84632.up.railway.app
- **GitHub Repository:** https://github.com/ImaanDuga/daily_quotes
- **Database:** PostgreSQL managed by Railway, `quote` table with 10 seeded records
- **Report:** This document
