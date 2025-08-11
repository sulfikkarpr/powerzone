# Powerzone Admin Mobile App (Gym Master - Phase 1)

Monorepo containing:
- `backend/`: FastAPI + PostgreSQL backend using psycopg2 (raw SQL)
- `mobile/`: React Native (Expo) admin app

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node 18+ and Yarn (for local mobile dev)
- Python 3.11+

### 1) Backend (Docker)

```bash
# from repo root
cp backend/.env.example backend/.env
# Edit backend/.env with your values (DB creds, JWT secret, WhatsApp Cloud API, UPI defaults)
docker compose up -d --build
# Run migrations
docker compose exec backend python -m app.scripts.init_db
# (optional) create first admin
docker compose exec backend python -m app.scripts.create_admin --name "Admin" --phone "+911234567890" --email "admin@example.com" --password "ChangeMe123"
```

API docs will be at `http://localhost:8000/docs`.

### 2) Mobile App

```bash
cd mobile
cp .env.example .env
yarn install
# Start the Expo dev server
yarn start
```

Login with the admin created above. Configure the API base URL in `mobile/.env`.

## Notes
- We added `amount` to the `payment_reminders` table to support revenue analytics.
- WhatsApp Cloud API requires `WHATSAPP_TOKEN` and `WHATSAPP_PHONE_NUMBER_ID`.
- UPI deep link uses `upi://pay` with configurable `UPI_ID`, `BUSINESS_NAME`, and optional `amount` and `note`.

## Monorepo Structure
```
backend/
  app/
    routers/
    scripts/
    __init__.py
    main.py
    db.py
    auth.py
    config.py
    schemas.py
  migrations/
    001_init.sql
  requirements.txt
  Dockerfile
  .env.example
mobile/
  src/
    screens/
    navigation/
    store/
    services/
    components/
    theme/
    App.tsx
  app.json
  package.json
  tsconfig.json
  babel.config.js
  .env.example
.dockerignore
.gitignore
README.md
```
