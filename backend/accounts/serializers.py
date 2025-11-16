from django.contrib.auth import authenticate
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from events.models import Event
from knowledge.models import Material
from news.models import NewsItem
from organizations.models import Organization

from .models import Favorite, User


class UserSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source="city.name", read_only=True)
    city_slug = serializers.CharField(source="city.slug", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "city",
            "city_name",
            "city_slug",
            "phone",
            "date_joined",
        )
        read_only_fields = ("username", "role", "date_joined")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "city",
            "phone",
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name", "role", "city", "phone")
        extra_kwargs = {
            "role": {"required": False},
            "city": {"required": False, "allow_null": True},
            "phone": {"required": False},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            username=attrs["username"],
            password=attrs["password"],
        )
        if not user:
            raise serializers.ValidationError("Неверный логин или пароль.")
        attrs["user"] = user
        return attrs


class FavoriteSerializer(serializers.ModelSerializer):
    target_type = serializers.ChoiceField(choices=[(m, m) for m in Favorite.ALLOWED_MODELS], write_only=True)
    target_id = serializers.IntegerField(write_only=True)
    preview = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ("id", "target_type", "target_id", "preview", "created_at")
        read_only_fields = ("id", "preview", "created_at")

    def _get_model(self, target_type: str):
        mapping = {
            "organization": Organization,
            "event": Event,
            "material": Material,
            "newsitem": NewsItem,
        }
        return mapping.get(target_type)

    def get_preview(self, obj: Favorite):
        target = obj.content_object
        if not target:
            return None
        data = {"type": obj.content_type.model, "id": obj.object_id}
        if isinstance(target, Organization):
            data.update(
                {
                    "title": target.name,
                    "city": target.city.name if target.city else None,
                    "slug": target.slug,
                }
            )
        elif isinstance(target, Event):
            data.update(
                {
                    "title": target.title,
                    "start_at": target.start_at,
                    "city": target.city.name if target.city else None,
                }
            )
        elif isinstance(target, Material):
            data.update({"title": target.title, "type": target.type})
        elif isinstance(target, NewsItem):
            data.update(
                {
                    "title": target.title,
                    "published_at": target.published_at,
                    "slug": target.slug,
                }
            )
        return data

    def validate(self, attrs):
        target_type = attrs.pop("target_type")
        target_model = self._get_model(target_type)
        if not target_model:
            raise serializers.ValidationError("Недопустимый тип объекта.")
        try:
            target = target_model.objects.get(pk=attrs["target_id"])
        except target_model.DoesNotExist:
            raise serializers.ValidationError("Объект не найден.")
        attrs["content_type"] = ContentType.objects.get_for_model(target_model)
        attrs["object_id"] = target.pk
        attrs["content_object"] = target
        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        favorite, _ = Favorite.objects.get_or_create(
            user=validated_data["user"],
            content_type=validated_data["content_type"],
            object_id=validated_data["object_id"],
            defaults={"content_object": validated_data.get("content_object")},
        )
        return favorite

