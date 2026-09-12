# CampusPulse Test Cases

| ID | Area | Scenario | Expected result |
| --- | --- | --- | --- |
| AUTH-01 | Auth | Register with valid details | 201 and JWT response |
| AUTH-02 | Auth | Register an existing email | 400 with duplicate message |
| AUTH-03 | Auth | Login with valid credentials | 200 with access/refresh |
| AUTH-04 | Auth | Login with wrong password | 400 validation response |
| AUTH-05 | Auth | Read profile with JWT | 200 with current user |
| CAT-01 | Category | Admin creates category | 201 |
| CAT-02 | Category | Duplicate category name | 400 |
| CAT-03 | Category | Admin edits/deletes category | 200/204 |
| EVT-01 | Event | Admin creates valid event | 201 and persisted event |
| EVT-02 | Event | End time before start time | 400 |
| EVT-03 | Event | Student creates event | 403 |
| EVT-04 | Event | Search/filter event list | Matching persisted rows only |
| REG-01 | Registration | Student registers | 201 persisted registration |
| REG-02 | Registration | Student registers twice | 409 and one row |
| REG-03 | Registration | Deadline passed | 400 |
| REG-04 | Registration | Capacity reached | 400 |
| REG-05 | Registration | Student cancels | 204 and status cancelled |
| REG-06 | Registration | Admin updates attendance | 200 |
| DASH-01 | Dashboard | Admin loads stats | Database-backed totals |

Automated coverage for the core registration, permissions, CRUD, authentication, and deadline cases is in `backend/core/tests.py` and runs with:

```bash
python backend/manage.py test core
```