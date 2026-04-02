# Practical Application of PaaS with Railway
### Cloud Computing – PaaS Practical Assignment

---

**Student Name:** Imaan Duga
**Course:** Cloud Computing
**Submission Date:** April 3, 2026
**Deployed Application URL:** https://web-production-84632.up.railway.app
**GitHub Repository:** https://github.com/ImaanDuga/daily_quotes

---

## 1. Introduction

This report documents the practical deployment of a web application on Railway, a Platform-as-a-Service (PaaS) provider. The application deployed is a Daily Quotes web app built using Python Flask. It allows users to view an inspirational quote of the day, and manage quotes through a full CRUD (Create, Read, Update, Delete) interface backed by a PostgreSQL database.

The assignment required demonstrating real-world cloud deployment skills including environment configuration, database integration, CI/CD automation, monitoring, and scalability planning.

---

## 2. Application Deployment

### 2.1 Application Overview

The Daily Quotes application is a Python Flask web application that:
- Displays a rotating quote of the day on the home page
- Allows users to add, edit, and delete quotes via a web interface
- Stores all quotes in a PostgreSQL database managed by Railway
- Automatically seeds the database with 10 default quotes on first deployment

### 2.2 Technology Stack

| Component     | Technology                  |
|---------------|-----------------------------|
| Backend       | Python Flask                |
| ORM           | Flask-SQLAlchemy            |
| Database      | PostgreSQL (Railway-managed)|
| Web Server    | Gunicorn                    |
| Frontend      | HTML, CSS, JavaScript       |
| Templating    | Jinja2                      |
| Version Control | GitHub                    |
| PaaS Platform | Railway                     |

### 2.3 Deployment Steps

**Step 1 – Local Development**
The application was developed and tested locally using SQLite as the development database. Environment variable support was built in from the start so the app could seamlessly switch between SQLite (local) and PostgreSQL (production) based on the `DATABASE_URL` environment variable.

**Step 2 – GitHub Repository**
The source code was pushed to a GitHub repository. A `.gitignore` file was configured to exclude sensitive files such as `.env` and the local SQLite database file, ensuring no credentials were exposed.

**Step 3 – Railway Project Setup**
A new project was created on Railway by connecting the GitHub repository directly. Railway automatically detected the Python application, installed all dependencies listed in `requirements.txt`, and used the `Procfile` to start the application using Gunicorn:

```
web: gunicorn app:app
```

**Step 4 – Database Provisioning**
A PostgreSQL database was provisioned from within the Railway dashboard by adding a new database service to the project. Railway automatically linked the database to the application by injecting the `DATABASE_URL` environment variable.

**Step 5 – Go Live**
After deployment, Railway provided a public URL:
`https://web-production-84632.up.railway.app`

The application was accessible immediately with all features functional.

---

## 3. Environment & Configuration Management

Sensitive configuration values are managed entirely through environment variables, following the 12-Factor App methodology. No credentials or secrets are hardcoded in the source code.

### 3.1 Environment Variables Used

| Variable       | Purpose                                      | Set By         |
|----------------|----------------------------------------------|----------------|
| `DATABASE_URL` | PostgreSQL connection string                 | Railway (auto) |
| `SECRET_KEY`   | Flask session encryption key                 | Manual (Railway Variables tab) |

### 3.2 Implementation

In `app.py`, the application reads these variables at startup:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///quotes.db")
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")
```

This ensures:
- Locally, the app uses SQLite with a default development key
- On Railway, it uses the production PostgreSQL database and a secure secret key
- The actual credentials never appear in the codebase

A `.env.example` file is included in the repository to document required variables without exposing their values.

---

## 4. Database Integration

### 4.1 Database Schema

The application uses a single table named `quote`:

| Column       | Data Type     | Constraints           | Description                  |
|--------------|---------------|-----------------------|------------------------------|
| id           | INTEGER       | PRIMARY KEY, NOT NULL | Auto-incrementing identifier |
| text         | VARCHAR(500)  | NOT NULL              | The quote content            |
| author       | VARCHAR(100)  | NOT NULL              | The quote author             |
| created_at   | DATETIME      | DEFAULT utcnow        | Timestamp of insertion       |

### 4.2 CRUD Operations

All four database operations are implemented:

| Operation | Route                      | Method     | Description                    |
|-----------|----------------------------|------------|--------------------------------|
| Create    | `/quotes/add`              | POST       | Insert a new quote             |
| Read      | `/` and `/quotes`          | GET        | Display quotes from database   |
| Update    | `/quotes/edit/<id>`        | GET / POST | Modify an existing quote       |
| Delete    | `/quotes/delete/<id>`      | POST       | Remove a quote from database   |

### 4.3 Sample Data

The database is automatically seeded with the following 10 quotes on first deployment:

| Author              | Quote (excerpt)                                              |
|---------------------|--------------------------------------------------------------|
| Steve Jobs          | "The only way to do great work is to love what you do."     |
| Albert Einstein     | "In the middle of every difficulty lies opportunity."        |
| Confucius           | "It does not matter how slowly you go..."                    |
| John Lennon         | "Life is what happens when you're busy making other plans." |
| Eleanor Roosevelt   | "The future belongs to those who believe..."                 |
| Winston Churchill   | "Success is not final, failure is not fatal..."              |
| Wayne Gretzky       | "You miss 100% of the shots you don't take."                |
| Henry Ford          | "Whether you think you can or you think you can't..."        |
| Chinese Proverb     | "The best time to plant a tree was 20 years ago..."          |
| Socrates            | "An unexamined life is not worth living."                    |

---

## 5. Scalability Awareness

### 5.1 Railway's Usage-Based Pricing Model

Railway charges based on actual resource consumption — CPU usage and RAM — rather than fixed monthly tiers. The Hobby plan provides $5 of free credit per month. Beyond that, usage is billed at approximately $0.000463 per vCPU per minute and $0.000231 per GB RAM per minute.

### 5.2 Impact of Increased Traffic

As the Daily Quotes application experiences more traffic, the following effects would occur:

| Traffic Level | Expected Impact                                                                 |
|---------------|---------------------------------------------------------------------------------|
| Low (< 100 users/day) | Current setup handles comfortably within free tier                   |
| Medium (1,000 users/day) | RAM usage increases, response times may slow slightly              |
| High (10,000+ users/day) | Single Gunicorn worker becomes a bottleneck, DB connections spike  |
| Very High (100,000+/day) | Requires horizontal scaling, caching layer, and DB upgrade         |

The main bottlenecks would be:
- **Single Gunicorn worker** — cannot handle many concurrent requests
- **Database connection pool** — PostgreSQL has a default connection limit
- **No caching** — every page load queries the database

### 5.3 Scaling Plan

1. **Increase Gunicorn workers** — change `Procfile` to `web: gunicorn app:app --workers 4` to handle more concurrent requests
2. **Vertical scaling** — increase RAM and CPU allocation in Railway's service settings
3. **Horizontal scaling** — enable multiple replicas in Railway to distribute incoming traffic across instances
4. **Add Redis caching** — cache the quote of the day to eliminate repeated database reads for the most visited page
5. **Database upgrade** — move to a higher PostgreSQL plan with increased connection limits and storage capacity
6. **CDN for static assets** — serve CSS and JavaScript files through a CDN to reduce load on the application server

---

## 6. CI/CD Workflow

### 6.1 Setup

The CI/CD pipeline was configured by connecting the GitHub repository to Railway during project setup. Railway uses a webhook to monitor the repository for changes.

### 6.2 Workflow

```
Developer pushes code → GitHub receives push → Railway webhook triggered
→ Railway pulls latest code → Rebuilds application → Redeploys automatically
→ New version live (typically within 60 seconds)
```

### 6.3 Verification

The CI/CD pipeline was verified multiple times during development:
- When database seeding was added, a `git push` triggered an automatic redeploy and the quotes appeared on the live site
- When the Edit/Update feature was added, pushing to GitHub automatically deployed the new functionality without any manual steps

This demonstrates a complete automated deployment pipeline with no manual intervention required after a code push.

---

## 7. Monitoring & Logging

### 7.1 Railway Logs

Railway provides real-time application logs accessible from the service dashboard under the "Logs" tab. Logs include application output, startup messages, request logs, and error traces.

### 7.2 Error Encountered and Resolved

**Error:** During initial deployment, the application failed to start with the following error visible in Railway logs:

```
sqlalchemy.exc.OperationalError: could not connect to server: Connection refused
Is the server running on host "localhost" and accepting TCP/IP connections on port 5432?
```

**Cause:** The application was attempting to connect to a database before the `DATABASE_URL` environment variable was properly configured in Railway's Variables tab.

**Resolution:** The Railway Variables tab was checked and the `DATABASE_URL` variable was confirmed and saved. A manual redeploy was triggered, after which the application connected to PostgreSQL successfully and started normally.

**Lesson:** Railway's logs provided the full stack trace immediately, making the root cause obvious. Without logging, this would have been difficult to diagnose.

---

## 8. Reflection & Comparison with Heroku

### 8.1 Deployment Experience on Railway

Overall, Railway provided a smooth and efficient deployment experience. The platform's GitHub integration made CI/CD setup trivial — connecting the repository and enabling auto-deploy took under two minutes. The automatic injection of `DATABASE_URL` when adding a PostgreSQL service eliminated a common source of configuration errors.

The most notable challenge was the initial database connection error described in Section 7, which was resolved quickly using Railway's logging tools.

### 8.2 Railway vs Heroku Comparison

| Feature                  | Railway                              | Heroku                                  |
|--------------------------|--------------------------------------|-----------------------------------------|
| Free tier                | $5/month credit included             | No free tier (discontinued Nov 2022)    |
| Deployment method        | Git push auto-deploy                 | Git push auto-deploy                    |
| Database                 | Postgres, MySQL, Redis built-in      | Postgres available as paid add-on       |
| Pricing model            | Usage-based (pay for what you use)   | Dyno-based fixed tiers                  |
| App sleep on inactivity  | No                                   | Yes (on lower tiers previously)         |
| Setup complexity         | Minimal, very intuitive              | Moderate, more configuration required   |
| Dashboard UI             | Modern, clean interface              | Mature but dated interface              |
| Custom domains           | Supported                            | Supported                               |
| Logging                  | Real-time in dashboard               | Real-time via CLI or dashboard          |

### 8.3 Conclusion

Railway is a strong choice for student projects and small-to-medium applications. Its usage-based pricing is more transparent and cost-effective than Heroku's fixed dyno tiers, especially for applications with variable or low traffic. The platform's simplicity — from GitHub integration to automatic database linking — significantly reduces the time spent on infrastructure and allows developers to focus on building the application itself.

Heroku remains a more mature platform with a larger ecosystem of add-ons, but its removal of the free tier in 2022 makes it less accessible for learning and experimentation. For this assignment, Railway fulfilled all requirements effectively and with minimal friction.

---

## 9. Deliverables Summary

| Deliverable                  | Details                                                        |
|------------------------------|----------------------------------------------------------------|
| Deployed Application URL     | https://web-production-84632.up.railway.app                   |
| Source Code Repository       | https://github.com/ImaanDuga/daily_quotes                     |
| Database Schema              | `quote` table — see Section 4.1                               |
| Sample Data                  | 10 seeded quotes — see Section 4.3                            |
| Documentation Report         | This document                                                  |

---

*End of Report*
