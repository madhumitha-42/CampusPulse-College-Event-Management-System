# Viva Questions and Answers

1. **What is CRUD?** Create, Read, Update, and Delete, the four basic data operations.
2. **Why React?** It enables reusable components and responsive state-driven interfaces.
3. **Why Django?** It provides a mature ORM, authentication ecosystem, routing, and security defaults.
4. **What is REST?** A resource-oriented HTTP API style using standard methods and status codes.
5. **What is DRF?** Django REST Framework adds serializers, permissions, viewsets, and API responses.
6. **What is an ORM?** A layer that maps application objects to database tables.
7. **Why SQLite?** It is portable and easy to demonstrate locally for a college project.
8. **What is JWT?** A signed token carrying claims used to authenticate API requests.
9. **Authentication vs authorization?** Authentication identifies a user; authorization decides what they may do.
10. **What is a foreign key?** A relationship from one table to a record in another table.
11. **Why a unique constraint?** It gives database-level protection against duplicate registrations.
12. **How are duplicates prevented?** The view checks first, then the unique constraint protects concurrent inserts.
13. **How does capacity work?** Only active registered rows count against the event capacity.
14. **Where is validation implemented?** Both browser forms and Django serializers validate inputs.
15. **What does GET do?** Reads a resource.
16. **What does POST do?** Creates a resource or invokes a creation action.
17. **What does PATCH do?** Partially updates a resource.
18. **What does DELETE do?** Removes or cancels a resource.
19. **What is 200?** Successful request.
20. **What is 201?** Resource successfully created.
21. **What is 400?** Invalid input or business-rule failure.
22. **What is 401?** Authentication is missing or invalid.
23. **What is 403?** The user is authenticated but lacks permission.
24. **What is 404?** The requested resource does not exist.
25. **What is 409?** The request conflicts with existing state, such as duplicate registration.
26. **How does the frontend call the backend?** Generated React Query hooks send JSON requests to `/api`.
27. **Why migrations?** They version database schema changes reproducibly.
28. **How do roles work?** The custom user model stores `ADMIN` or `STUDENT`; DRF permissions enforce actions.
29. **How are dashboard numbers kept real?** Statistics are calculated from ORM queries on every request.
30. **How are tests organized?** Django API tests create isolated data and assert response codes and persistence.
31. **Why use GitHub?** It preserves history, supports collaboration, and makes the submission reproducible.
32. **What could be improved?** Email reminders, QR check-in, calendar sync, pagination, and event images.