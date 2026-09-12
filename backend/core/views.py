from datetime import datetime

from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Event, Registration, User
from .permissions import IsAdmin, IsStudent
from .serializers import (
    CategorySerializer,
    EventSerializer,
    LoginSerializer,
    RegisterSerializer,
    RegistrationSerializer,
    RegistrationUpdateSerializer,
    UserSerializer,
)


def token_response(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": UserSerializer(user).data,
    }


@api_view(["GET"])
@permission_classes([AllowAny])
def healthz(request):
    return Response({"status": "ok"})


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response(token_response(user), status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(token_response(serializer.validated_data["user"]))


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh(request):
    token = RefreshToken(request.data.get("refresh", ""))
    return Response({"access": str(token.access_token)})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.annotate(event_count=Count("events")).all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        return [IsAdmin()] if self.action in ["create", "update", "partial_update", "destroy"] else [AllowAny()]

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"error": "This category is still used by an event and cannot be deleted."},
                status=status.HTTP_409_CONFLICT,
            )


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related("category").all()
    serializer_class = EventSerializer

    def get_permissions(self):
        return [IsAdmin()] if self.action in ["create", "update", "partial_update", "destroy"] else [AllowAny()]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        search = params.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(venue__icontains=search)
                | Q(organizer__icontains=search)
            )
        if params.get("category"):
            queryset = queryset.filter(category_id=params["category"])
        if params.get("status"):
            queryset = queryset.filter(status=params["status"])
        if params.get("date"):
            queryset = queryset.filter(date=params["date"])
        ordering = params.get("ordering", "date")
        allowed = {"date", "-date", "title", "-title", "-created_at"}
        return queryset.order_by(ordering if ordering in allowed else "date")


@api_view(["POST"])
@permission_classes([IsStudent])
def register_for_event(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)
    if event.status == Event.Status.CANCELLED:
        return Response({"error": "Cancelled events cannot accept registrations."}, status=status.HTTP_400_BAD_REQUEST)
    if timezone.now() > event.registration_deadline:
        return Response({"error": "The registration deadline has passed."}, status=status.HTTP_400_BAD_REQUEST)
    registered_count = Registration.objects.filter(event=event, status=Registration.Status.REGISTERED).count()
    if registered_count >= event.capacity:
        return Response({"error": "This event has reached its capacity."}, status=status.HTTP_400_BAD_REQUEST)
    if Registration.objects.filter(student=request.user, event=event).exists():
        return Response({"error": "You are already registered for this event."}, status=status.HTTP_409_CONFLICT)
    try:
        with transaction.atomic():
            registration = Registration.objects.create(student=request.user, event=event)
    except IntegrityError:
        return Response({"error": "You are already registered for this event."}, status=status.HTTP_409_CONFLICT)
    return Response(RegistrationSerializer(registration).data, status=status.HTTP_201_CREATED)


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.select_related("student", "event", "event__category").all()
    serializer_class = RegistrationSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve", "destroy", "update", "partial_update"]:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role != User.Roles.ADMIN:
            queryset = queryset.filter(student=self.request.user)
        return queryset

    def get_serializer_class(self):
        return RegistrationUpdateSerializer if self.action in ["update", "partial_update"] else RegistrationSerializer

    def update(self, request, *args, **kwargs):
        if request.user.role != User.Roles.ADMIN:
            return Response({"error": "Only administrators can update attendance status."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        registration = self.get_object()
        if request.user.role != User.Roles.ADMIN and registration.student_id != request.user.id:
            return Response({"error": "You can only cancel your own registration."}, status=status.HTTP_403_FORBIDDEN)
        registration.status = Registration.Status.CANCELLED
        registration.save(update_fields=["status"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyRegistrationsView(ListAPIView):
    permission_classes = [IsStudent]
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        return RegistrationViewSet.queryset.filter(student=self.request.user)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    events = Event.objects.select_related("category")
    registered = Registration.objects.filter(status=Registration.Status.REGISTERED)
    if request.user.role == User.Roles.ADMIN:
        return Response({
            "total_events": events.count(),
            "upcoming_events": events.filter(status=Event.Status.UPCOMING).count(),
            "completed_events": events.filter(status=Event.Status.COMPLETED).count(),
            "cancelled_events": events.filter(status=Event.Status.CANCELLED).count(),
            "total_students": User.objects.filter(role=User.Roles.STUDENT).count(),
            "total_registrations": registered.count(),
            "recent_events": EventSerializer(events.order_by("-created_at")[:5], many=True).data,
            "my_registrations": 0,
            "available_events": events.filter(status=Event.Status.UPCOMING).count(),
        })
    return Response({
        "total_events": events.count(),
        "upcoming_events": events.filter(status=Event.Status.UPCOMING).count(),
        "completed_events": 0,
        "cancelled_events": 0,
        "total_students": 0,
        "total_registrations": Registration.objects.filter(student=request.user).count(),
        "recent_events": EventSerializer(events.order_by("-created_at")[:5], many=True).data,
        "my_registrations": Registration.objects.filter(student=request.user).count(),
        "available_events": events.filter(status=Event.Status.UPCOMING).count(),
    })