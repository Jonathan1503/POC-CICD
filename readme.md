# Blacklist API

This microservice allows centralized management of a global email blacklist across multiple internal systems. It enables adding emails to the blacklist and querying whether an email is blacklisted, using a secure JWT-based REST API with PostgreSQL for persistence.

---

## Features
- **POST /blacklists**: Add an email to the blacklist with app UUID, optional block reason, IP, and timestamp.
- **GET /blacklists/<email>**: Check if an email is blacklisted.
- **JWT Authentication**: All endpoints require a static Bearer token.
- **Input validation** using Marshmallow (email format, UUID format, max length).

---

## Tech Stack
- Python 3.8+
- Flask (latest)
- Flask-RESTful, Flask-JWT-Extended
- Flask-SQLAlchemy + PostgreSQL
- Marshmallow for serialization/validation
- Docker (only for PostgreSQL)

---

## Setup

This setup runs the application locally and the PostgreSQL database in a Docker container.

### Steps:
```bash
git clone <repo-url>
cd DevOps-Project

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run PostgreSQL via Docker
docker run --name postgres_db -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres:13

# Run the Flask app
python application.py
```

Make sure port `5432` is free before starting the container.

---

## Configuration
Values can be set via environment variables or in `config.py`:
- `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`
- `SECRET_KEY`, `JWT_SECRET_KEY`

_Default JWT secret is `token`._

---

## API Endpoints

### POST `/blacklists`
- **Auth:** `Bearer <JWT>`
- **JSON body:**
  ```json
  {
    "email": "example@domain.com",
    "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
    "blocked_reason": "Spam user"
  }
  ```
- **Responses:** `201 Created`, `400 Bad Request`, `401 Unauthorized`

### GET `/blacklists/<email>`
- **Auth:** `Bearer <JWT>`
- **Response:**
  ```json
  { "is_blacklisted": true, "blocked_reason": "Spam user" }
  ```
  Or:
  ```json
  { "is_blacklisted": false }
  ```

---

## Postman Collection
Use the file: `postman/Blacklist API.postman_collection.json`

**Recommended order:**
1. Add email to blacklist (valid)
2. Try duplicate (400)
3. Invalid email (400)
4. Invalid UUID (400)
5. No auth (401)
6. Query blacklisted email (200)
7. Query non-blacklisted email (200)
8. Query without auth (401)

Set the `jwt_token` variable in Postman with a valid token signed using the secret `token`.

---

## Troubleshooting
- **"Signature verification failed"**: Your JWT does not match `JWT_SECRET_KEY`.
- **"Missing Authorization Header"**: Ensure you include the Bearer token.
- **Database connection error**: Check that your PostgreSQL container is running. On Windows, use `host.docker.internal` as the host if needed.

---

## License
Free to use for academic and demo purposes.
