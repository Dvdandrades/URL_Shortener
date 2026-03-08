# URL Shortener

A FastAPI-based URL shortener with a built-in web UI. Shorten URLs, use custom keys, peek at targets without redirecting, and delete links via secret keys.

## Features

- **Shorten URLs** — generates a random 5-character key for any valid URL
- **Custom keys** — optionally choose your own short key instead of a random one
- **Peek** — check where a short URL points without being redirected
- **Graceful forward** — verifies the target is reachable before redirecting (returns `502` if not)
- **Soft delete** — deactivate shortened URLs via their secret key
- **Web UI** — single-page interface served directly by FastAPI

## Project Structure

```
shortener_app/
├── __init__.py
├── config.py       # Settings via pydantic-settings, supports .env
├── crud.py         # Database operations
├── database.py     # SQLAlchemy engine and session
├── keygen.py       # Random and unique key generation
├── main.py         # FastAPI app, routes, and static file serving
├── models.py       # SQLAlchemy URL model
├── schemas.py      # Pydantic schemas
└── static/
    └── index.html  # Web UI
```

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended)

## Installation

```bash
git clone https://github.com/Dvdandrades/URL_Shortener.git
cd Url_short
uv sync
```

## Running

```bash
uvicorn shortener_app.main:app --reload
```

The app will be available at `http://localhost:8000`.

## Configuration

Create a `.env` file in the project root to override defaults:

```env
ENV_NAME=Production
BASE_URL=https://your-domain.com
DB_URL=sqlite:///./shortener.db
```

## API Reference

### `POST /url`
Create a shortened URL.

**Body:**
```json
{
  "target_url": "https://example.com",
  "custom_url": "my-key"
}
```
`custom_url` is optional. Allowed characters: letters, digits, `. _ ~ -`

**Response:**
```json
{
  "url": "http://localhost:8000/my-key",
  "admin_url": "http://localhost:8000/admin/my-key_XXXXXXXX",
  "target_url": "https://example.com",
  "is_active": true,
  "clicks": 0
}
```

---

### `GET /{url_key}`
Redirect to the target URL. Verifies the target is reachable first.

- `302` — redirects to target
- `404` — key not found
- `502` — target URL is unreachable

---

### `GET /{url_key}/peek`
Returns the target URL without redirecting.

```json
{ "target_url": "https://example.com" }
```

---

### `GET /admin/{secret_key}`
Returns full info about a shortened URL including click count.

---

### `DELETE /admin/{secret_key}`
Deactivates a shortened URL. The key remains reserved — it cannot be reused.

---

## Design Notes

- **Soft deletes** — URLs are deactivated (`is_active = False`), never removed from the database. This means a deleted custom key cannot be re-registered.
- **Graceful forward** — uses an HTTP `HEAD` request to check target reachability with minimal bandwidth before redirecting.
- **Secret key** — formatted as `{key}_{8-char-random}`, returned only at creation time. Store it if you want to manage your link later.

## Interactive Docs

FastAPI's auto-generated docs are available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`