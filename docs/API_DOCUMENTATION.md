# CampusPulse API Documentation

Base URL: `/api`

Private endpoints use `Authorization: Bearer <access-token>`.

## Authentication

| Method | URL | Auth | Purpose |
| --- | --- | --- | --- |
| POST | `/auth/register/` | Public | Create a student account |
| POST | `/auth/login/` | Public | Return access, refresh, and user data |
| POST | `/auth/refresh/` | Public | Return a new access token |
| GET | `/auth/me/` | JWT | Return the current profile |

Register body: `{"name":"Mira Shah","email":"mira@example.com","password":"StudentPass!123"}`.
Login body: `{"email":"mira@example.com","password":"StudentPass!123"}`.

## Categories

| Method | URL | Role | Purpose |
| --- | --- | --- | --- |
| GET | `/categories/` | Public | List categories |
| POST | `/categories/` | Admin | Create category |
| GET | `/categories/{id}/` | Public | Category detail |
| PATCH | `/categories/{id}/` | Admin | Update category |
| DELETE | `/categories/{id}/` | Admin | Delete category |

Category body: `{"name":"Technology","description":"Build and explore."}`.

## Events

| Method | URL | Role | Purpose |
| --- | --- | --- | --- |
| GET | `/events/` | Public | List, search, filter, and order events |
| POST | `/events/` | Admin | Create event |
| GET | `/events/{id}/` | Public | Event detail |
| PATCH | `/events/{id}/` | Admin | Update event |
| DELETE | `/events/{id}/` | Admin | Delete event |

Query parameters: `search`, `category`, `status`, `date`, and `ordering` (`date`, `-date`, `title`, `-title`, `-created_at`).

Event body:

```json
{
  "title": "AI & Ethics Forum",
  "description": "A student-led forum.",
  "category": 1,
  "date": "2026-10-12",
  "start_time": "10:00",
  "end_time": "12:00",
  "venue": "Main Auditorium",
  "organizer": "Student Activities Council",
  "capacity": 120,
  "registration_deadline": "2026-10-11T18:00:00Z",
  "status": "UPCOMING"
}
```

## Registrations

| Method | URL | Role | Purpose |
| --- | --- | --- | --- |
| POST | `/events/{id}/register/` | Student | Register for an event |
| GET | `/registrations/my/` | Student | List own registrations |
| GET | `/registrations/` | Admin | List all participants |
| GET | `/registrations/{id}/` | Authenticated | Registration detail |
| PATCH | `/registrations/{id}/` | Admin | Set `REGISTERED`, `CANCELLED`, `ATTENDED`, or `ABSENT` |
| DELETE | `/registrations/{id}/` | Owner/Admin | Cancel registration |

Registration returns `400` for cancelled events, passed deadlines, or full capacity and `409` for duplicate registration.

## Dashboard

`GET /dashboard/stats/` returns real event, student, registration, recent-event, and availability counts. The shape is role-aware: admins receive coordinator totals; students receive their own registration counts.

## Common status codes

`200` success, `201` created, `204` deleted/cancelled, `400` validation/business rule error, `401` missing or invalid JWT, `403` role restriction, `404` missing resource, `409` duplicate registration.