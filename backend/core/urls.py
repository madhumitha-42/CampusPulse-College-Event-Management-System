from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    EventViewSet,
    MyRegistrationsView,
    RegistrationViewSet,
    dashboard_stats,
    healthz,
    login,
    me,
    refresh,
    register,
    register_for_event,
)

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("events", EventViewSet, basename="event")
router.register("registrations", RegistrationViewSet, basename="registration")

urlpatterns = [
    path("healthz", healthz),
    path("auth/register/", register),
    path("auth/login/", login),
    path("auth/refresh/", refresh),
    path("auth/me/", me),
    path("events/<int:pk>/register/", register_for_event),
    path("registrations/my/", MyRegistrationsView.as_view()),
    path("dashboard/stats/", dashboard_stats),
    path("", include(router.urls)),
]