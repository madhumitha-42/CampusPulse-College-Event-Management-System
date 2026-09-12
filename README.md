# CampusPulse

Smart College Event & Participation Management System — a real CRUD application for student event discovery, registration, and coordinator operations.

## Overview

CampusPulse replaces disconnected notices and spreadsheets with one shared calendar. Students can discover events, search by title or venue, filter by category and status, register, and cancel registrations. Coordinators can create, edit, delete, and organize events, manage categories, review participant rosters, update attendance status, and see live dashboard statistics.

## Objectives

- Demonstrate complete Create, Read, Update, and Delete workflows.
- Apply secure JWT authentication and role-based access for administrators and students.
- Use relational database models, foreign keys, migrations, and a database-level duplicate-registration constraint.
- Provide a responsive, polished React experience backed by real Django APIs.
- Supply a GitHub-ready college submission with tests, API documentation, report material, and a Postman collection.

## Technology stack

| Layer | Technology |
| --- | --- |
| Frontend | React, Vite, TypeScript, Wouter, Tailwind CSS |
| Backend | Python, Django 5.2, Django REST Framework |
| Authentication | JWT with `djangorestframework-simplejwt` |
| Database | SQLite and Django ORM |
| API contract | OpenAPI 3.1 with Orval-generated React Query hooks |
| Testing | Django `APITestCase` |

## Features

- Public landing page, login, and student registration.
- Role-aware student and coordinator dashboards.
- Event CRUD with date, time, capacity, deadline, status, category, and validation.
- Category CRUD with duplicate-name validation.
- Event discovery with backend-powered search, category/status/date filters, and ordering.
- Student registration, duplicate protection, capacity/deadline/cancellation checks, and registration history.
- Coordinator participant management with attendance status updates.
- Responsive navigation, tables, cards, loading states, empty states, error messages, and destructive-action confirmations.

## Project structure

```text
backend/
  manage.py
  config/
  core/
    models.py
    serializers.py
    views.py
    tests.py
    migrations/
artifacts/college-events/     React/Vite frontend
lib/api-spec/openapi.yaml     API contract
lib/api-client-react/         generated React Query client
docs/                         report and submission documentation
```

## Setup and run

The Python dependencies are listed in `backend/requirements.txt`. In this Replit workspace they are installed into `.pythonlibs`.

```bash
python backend/manage.py migrate
python backend/manage.py load_demo_data
```

Run the two services:

```bash
pnpm --filter @workspace/api-server run dev
pnpm --filter @workspace/college-events run dev
```

Use the Replit preview for the frontend. The frontend calls the Django API through `/api`.

### Environment variables

Copy `backend/.env.example` when running outside Replit:

```env
DJANGO_SECRET_KEY=replace-me
DJANGO_DEBUG=1
```

Never commit `.env`, passwords, or JWT secrets.

## Demo accounts

The `load_demo_data` command creates fictional accounts for a college demonstration:

- Coordinator: `admin@campuspulse.demo` / `CampusDemo!2026`
- Student: `mira@campuspulse.demo` / `StudentDemo!2026`
- Additional students use the same student password.

Change or remove these accounts before any real deployment.

## Tests and code generation

```bash
python backend/manage.py test core
pnpm --filter @workspace/college-events run typecheck
pnpm --filter @workspace/api-spec run codegen
pnpm run typecheck
```

The OpenAPI document is the source of truth. Re-run codegen whenever the API contract changes.

## Documentation

- [Project report](docs/PROJECT_REPORT.md)
- [API documentation](docs/API_DOCUMENTATION.md)
- [Test cases](docs/TEST_CASES.md)
- [ER diagram](docs/ER_DIAGRAM.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Demo guide](docs/DEMO_GUIDE.md)
- [Viva questions](docs/VIVA_QUESTIONS.md)
- [SOP mapping](docs/SOP_MAPPING.md)
- [Postman collection](docs/postman/CampusPulse.postman_collection.json)

## Future enhancements

Email reminders, QR-based check-in, image uploads for event posters, pagination for large campuses, calendar export, and analytics by department are natural next steps.