# SOP Mapping

| Requirement | CampusPulse implementation |
| --- | --- |
| Frontend UI | `artifacts/college-events/src/App.tsx` provides public, student, and coordinator routes with responsive UI. |
| Backend/API | `backend/core/views.py`, `serializers.py`, and `urls.py` implement REST endpoints. |
| Database | `backend/core/models.py` defines User, Category, Event, and Registration with migrations. |
| CRUD | Event and Category model viewsets provide create, read, update, delete. |
| Validation | React required fields plus DRF serializer rules for duplicates, times, deadlines, and capacity. |
| Exception handling | API status codes and frontend error/empty/loading states cover invalid, unauthorized, missing, and conflict paths. |
| Testing | `backend/core/tests.py` covers auth boundaries, CRUD, registration, duplicate, deadline, and permissions. |
| Git/GitHub | Root `.gitignore`, requirements file, generated API contract, and clean backend/frontend split. |
| Documentation | README, API reference, report, architecture, ER diagram, test cases, viva, and demo guide. |
| Demo | `load_demo_data` supplies fictional accounts, categories, events, and registrations. |

## CRUD evidence

- Create event: `POST /api/events/`
- Read events: `GET /api/events/` and `GET /api/events/{id}/`
- Update event: `PATCH /api/events/{id}/`
- Delete event: `DELETE /api/events/{id}/`
- Registration create: `POST /api/events/{id}/register/`
- Registration cancel: `DELETE /api/registrations/{id}/`