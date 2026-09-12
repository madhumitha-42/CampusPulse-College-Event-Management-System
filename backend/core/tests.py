from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from .models import Category, Event, Registration, User


class CampusPulseApiTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin@example.com", "Admin", "AdminPass!123", role="ADMIN")
        self.student = User.objects.create_user("student@example.com", "Student", "StudentPass!123")
        self.category = Category.objects.create(name="Technology", description="Tech events")
        self.event = Event.objects.create(
            title="Demo Event",
            description="A useful event",
            category=self.category,
            date=(timezone.now() + timedelta(days=5)).date(),
            start_time="10:00",
            end_time="12:00",
            venue="Auditorium",
            organizer="Council",
            capacity=2,
            registration_deadline=timezone.now() + timedelta(days=2),
        )

    def auth(self, user):
        from rest_framework_simplejwt.tokens import RefreshToken

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(user).access_token}")

    def test_student_registration_and_duplicate_protection(self):
        self.auth(self.student)
        response = self.client.post(f"/api/events/{self.event.id}/register/")
        self.assertEqual(response.status_code, 201)
        duplicate = self.client.post(f"/api/events/{self.event.id}/register/")
        self.assertEqual(duplicate.status_code, 409)
        self.assertEqual(Registration.objects.count(), 1)

    def test_student_cannot_create_event(self):
        self.auth(self.student)
        response = self.client.post("/api/events/", {})
        self.assertEqual(response.status_code, 403)

    def test_admin_can_create_update_delete_event(self):
        self.auth(self.admin)
        payload = {
            "title": "New Event",
            "description": "New description",
            "category_id": self.category.id,
            "date": str((timezone.now() + timedelta(days=8)).date()),
            "start_time": "13:00",
            "end_time": "14:00",
            "venue": "Lab",
            "organizer": "Council",
            "capacity": 50,
            "registration_deadline": (timezone.now() + timedelta(days=6)).isoformat(),
        }
        created = self.client.post("/api/events/", payload, format="json")
        self.assertEqual(created.status_code, 201)
        event_id = created.data["id"]
        updated = self.client.patch(f"/api/events/{event_id}/", {"title": "Renamed"}, format="json")
        self.assertEqual(updated.status_code, 200)
        deleted = self.client.delete(f"/api/events/{event_id}/")
        self.assertEqual(deleted.status_code, 204)

    def test_registration_requires_student_auth(self):
        response = self.client.post(f"/api/events/{self.event.id}/register/")
        self.assertEqual(response.status_code, 401)

    def test_registration_deadline_is_enforced(self):
        self.event.registration_deadline = timezone.now() - timedelta(minutes=1)
        self.event.save(update_fields=["registration_deadline"])
        self.auth(self.student)
        response = self.client.post(f"/api/events/{self.event.id}/register/")
        self.assertEqual(response.status_code, 400)