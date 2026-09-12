# Smart College Event & Participation Management System

## 1. Introduction

CampusPulse is a full-stack web application that makes college event discovery and participation easier for students and coordinators.

## 2. Problem statement

College activities are often distributed across notices, chats, and spreadsheets. Students miss opportunities and coordinators lack one reliable view of attendance.

## 3. Objectives

The system centralizes event CRUD, student registration, role-based access, capacity checks, search, filtering, dashboards, and documentation in one demonstrable application.

## 4. Proposed solution

React provides the responsive interface. Django REST Framework exposes authenticated APIs. Django ORM stores users, categories, events, and registrations in SQLite.

## 5. System features

Public event discovery, JWT login, student registration, coordinator dashboards, category/event CRUD, registration cancellation, participant management, search/filter/sort, validation, and error states.

## 6. Technology stack

React, Vite, TypeScript, Wouter, Tailwind CSS, Python, Django, Django REST Framework, SimpleJWT, SQLite, OpenAPI, Orval, and Django tests.

## 7. Architecture and database design

See [ARCHITECTURE.md](ARCHITECTURE.md) and [ER_DIAGRAM.md](ER_DIAGRAM.md). The model relationships are Category 1:N Event, User 1:N Registration, and Event 1:N Registration.

## 8. Module description

- Authentication module: register, login, refresh, profile.
- Event module: discovery and coordinator CRUD.
- Category module: taxonomy CRUD.
- Registration module: business-rule checks and participant status.
- Dashboard module: role-aware ORM aggregates.

## 9. CRUD implementation

Event and category viewsets expose list, detail, create, update, and delete operations. Registration uses an action endpoint for student signup and a viewset for participant management.

## 10. Authentication and authorization

SimpleJWT signs access and refresh tokens. `IsAdmin` restricts management APIs and `IsStudent` restricts event signup. Passwords use Django's secure password hashing.

## 11. Validation and exception handling

Serializers validate email uniqueness, password length, event time ordering, positive capacity, deadline logic, and supported statuses. The frontend shows actionable error, loading, and empty states.

## 12. Testing and results

The backend suite covers duplicate registration, student restrictions, admin event CRUD, unauthenticated registration, and passed deadlines. The documented test run passes.

## 13. Challenges

Keeping generated API types, a separate Django implementation, and responsive role-specific screens aligned required a contract-first OpenAPI document and explicit cache invalidation after mutations.

## 14. Future enhancements

Email notifications, QR check-in, event images, calendar integration, pagination, and department analytics.

## 15. Conclusion

CampusPulse demonstrates a complete, real CRUD web application suitable for a college demonstration, viva, repository, and report.