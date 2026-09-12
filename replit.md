# CampusPulse

CampusPulse is a full-stack college event and participation management system for students and campus coordinators.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the Django API server through the `/api` service
- `pnpm --filter @workspace/college-events run dev` — run the React/Vite frontend
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `python backend/manage.py migrate` — apply Django migrations
- `python backend/manage.py load_demo_data` — load fictional demo accounts, categories, events, and registrations
- `python backend/manage.py test core` — run backend tests

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- Frontend: React, Vite, TypeScript, Wouter, Tailwind CSS
- API: Django 5.2, Django REST Framework, SimpleJWT
- DB: SQLite + Django ORM + migrations
- API contract: OpenAPI, Orval-generated React Query hooks and Zod schemas

## Where things live

- `backend/` — Django project, custom user model, API views, migrations, tests, and demo command
- `artifacts/college-events/` — React/Vite frontend and responsive CampusPulse UI
- `lib/api-spec/openapi.yaml` — API contract source of truth
- `lib/api-client-react/` — generated frontend hooks
- `docs/` — report, architecture, API reference, testing, demo guide, viva, SOP mapping, and Postman

## Architecture decisions

- SQLite is intentional for simple local college-project setup; the ORM keeps the schema portable.
- The API server artifact runs the Django service so the existing `/api` proxy remains the single browser-facing backend path.
- Event and registration rules are enforced in serializers, service views, and database constraints.

## Product

Students discover, search, filter, and register for events. Coordinators manage categories, events, registrations, attendance status, and live dashboard counts.

## User preferences

The submitted brief requires a real Django + React CRUD system with documentation and a Postman collection.

## Gotchas

- Run migrations before loading demo data.
- Regenerate client hooks after editing `lib/api-spec/openapi.yaml`.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
