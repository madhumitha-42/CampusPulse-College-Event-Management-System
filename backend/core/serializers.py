from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers

from .models import Category, Event, Registration, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "role", "created_at"]
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["name", "email", "password"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value.lower()

    def create(self, validated_data):
        return User.objects.create_user(role=User.Roles.STUDENT, **validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(email=attrs["email"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")
        attrs["user"] = user
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    event_count = serializers.IntegerField(source="events.count", read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "description", "created_at", "event_count"]
        read_only_fields = ["id", "created_at", "event_count"]


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class EventSerializer(serializers.ModelSerializer):
    category = EventCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source="category", queryset=Category.objects.all(), write_only=True, required=False
    )
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id", "title", "description", "category", "category_id", "date",
            "start_time", "end_time", "venue", "organizer", "capacity",
            "registration_deadline", "status", "created_at", "updated_at",
            "participant_count",
        ]
        read_only_fields = ["id", "category", "created_at", "updated_at", "participant_count"]

    def to_internal_value(self, data):
        # The public API uses `category`; keep the response nested while
        # accepting the numeric category id used by event forms.
        payload = data.copy()
        if "category" in payload and "category_id" not in payload:
            payload["category_id"] = payload.pop("category")
        return super().to_internal_value(payload)

    def get_participant_count(self, obj):
        return obj.registrations.filter(status=Registration.Status.REGISTERED).count()

    def validate(self, attrs):
        start = attrs.get("start_time", getattr(self.instance, "start_time", None))
        end = attrs.get("end_time", getattr(self.instance, "end_time", None))
        if start and end and end <= start:
            raise serializers.ValidationError({"end_time": "End time must be later than start time."})
        capacity = attrs.get("capacity", getattr(self.instance, "capacity", None))
        if capacity is not None and capacity <= 0:
            raise serializers.ValidationError({"capacity": "Capacity must be a positive number."})
        deadline = attrs.get(
            "registration_deadline", getattr(self.instance, "registration_deadline", None)
        )
        event_date = attrs.get("date", getattr(self.instance, "date", None))
        if deadline and event_date and deadline.date() > event_date:
            raise serializers.ValidationError(
                {"registration_deadline": "Registration deadline cannot be after the event date."}
            )
        return attrs


class RegistrationSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)

    class Meta:
        model = Registration
        fields = ["id", "student", "event", "registration_date", "status"]
        read_only_fields = ["id", "student", "event", "registration_date"]


class RegistrationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ["status"]

    def validate_status(self, value):
        if value not in Registration.Status.values:
            raise serializers.ValidationError("Unsupported registration status.")
        return value