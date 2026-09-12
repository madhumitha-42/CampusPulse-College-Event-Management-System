from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Category, Event, Registration, User


class Command(BaseCommand):
    help = "Load fictional CampusPulse demo data."

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(
            email="admin@campuspulse.demo",
            defaults={"name": "Aarav Nair", "role": User.Roles.ADMIN, "is_staff": True, "is_superuser": True},
        )
        admin.set_password("CampusDemo!2026")
        admin.role = User.Roles.ADMIN
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

        students = []
        for name, email in [
            ("Mira Shah", "mira@campuspulse.demo"),
            ("Rohan Iyer", "rohan@campuspulse.demo"),
            ("Diya Menon", "diya@campuspulse.demo"),
        ]:
            student, _ = User.objects.get_or_create(email=email, defaults={"name": name})
            student.set_password("StudentDemo!2026")
            student.save()
            students.append(student)

        category_data = [
            ("Technology", "Build, code, and explore the ideas shaping tomorrow."),
            ("Culture & Arts", "Performances, showcases, and creative campus life."),
            ("Leadership", "Conversations and workshops for confident changemakers."),
            ("Wellness", "Activities that help the campus community feel its best."),
        ]
        categories = {name: Category.objects.get_or_create(name=name, defaults={"description": description})[0] for name, description in category_data}
        now = timezone.now()
        event_data = [
            ("AI & Ethics Forum", "A student-led forum on building responsible AI systems.", "Technology", 120, 12),
            ("Open Mic Under the Stars", "An evening of poetry, acoustic sets, and short stories.", "Culture & Arts", 180, 19),
            ("Design Your First Startup", "A hands-on workshop with founders from the local ecosystem.", "Leadership", 80, 8),
            ("Sunrise Yoga on the Lawn", "A guided session to start the semester with energy.", "Wellness", 60, 6),
        ]
        events = []
        for title, description, category, capacity, day in event_data:
            event, _ = Event.objects.get_or_create(
                title=title,
                defaults={
                    "description": description,
                    "category": categories[category],
                    "date": (now + timedelta(days=day)).date(),
                    "start_time": datetime.strptime("10:00", "%H:%M").time(),
                    "end_time": datetime.strptime("12:00", "%H:%M").time(),
                    "venue": "Main Campus",
                    "organizer": "Student Activities Council",
                    "capacity": capacity,
                    "registration_deadline": now + timedelta(days=max(day - 1, 1)),
                },
            )
            events.append(event)
        for student, event in zip(students, events):
            Registration.objects.get_or_create(student=student, event=event)
        self.stdout.write(self.style.SUCCESS("CampusPulse demo data loaded."))