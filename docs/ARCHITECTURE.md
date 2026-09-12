# CampusPulse Architecture

## Request flow

```text
Student or coordinator
        ↓
React/Vite frontend
        ↓  JWT Bearer token + JSON
REST API at /api
        ↓
Django REST Framework
        ↓
Django serializers, permissions, and viewsets
        ↓
Django ORM
        ↓
SQLite database
```

The frontend uses the generated client in `lib/api-client-react`. Authentication stores the short-lived access token and refresh token in browser storage for the demonstration and attaches the access token to API requests. The backend validates the token with SimpleJWT before private views execute.

## Main modules

- `User`: custom email-login user with `ADMIN` and `STUDENT` roles.
- `Category`: unique event taxonomy.
- `Event`: event details, scheduling, capacity, deadline, and lifecycle status.
- `Registration`: student/event join record with a unique `(student, event)` constraint.

## CRUD flow

Coordinator forms call POST/PATCH/DELETE event or category endpoints. Django serializers validate required fields, time ordering, capacity, and deadlines before Django ORM writes. React Query invalidates affected lists and detail caches after successful mutations.

## Registration flow

The registration view checks identity, role, event status, deadline, current capacity, and prior registration. The final insert is protected by the database unique constraint, so concurrent duplicate requests still fail safely.