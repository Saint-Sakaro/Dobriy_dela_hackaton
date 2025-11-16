import requests
from django.conf import settings
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Favorite, User
from .serializers import (
    FavoriteSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    UserSerializer,
)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user": UserSerializer(user, context={"request": request}).data},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": UserSerializer(user, context={"request": request}).data})


class VKLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        access_token = request.data.get("access_token")
        if not access_token:
            return Response({"detail": "Токен VK не предоставлен."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Получаем данные пользователя из VK API
            vk_response = requests.get(
                "https://api.vk.com/method/users.get",
                params={
                    "access_token": access_token,
                    "v": "5.131",
                    "fields": "email,phone",
                },
                timeout=5,
            )
            vk_data = vk_response.json()

            if "error" in vk_data:
                return Response(
                    {"detail": "Ошибка VK API: " + vk_data["error"].get("error_msg", "Неизвестная ошибка")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            vk_user = vk_data["response"][0]
            vk_id = str(vk_user["id"])
            email = vk_user.get("email") or f"vk_{vk_id}@vk.id"
            username = f"vk_{vk_id}"

            # Создаём или получаем пользователя
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": vk_user.get("first_name", ""),
                    "last_name": vk_user.get("last_name", ""),
                },
            )

            if not created:
                # Обновляем данные, если пользователь уже существует
                user.email = email
                if vk_user.get("first_name"):
                    user.first_name = vk_user["first_name"]
                if vk_user.get("last_name"):
                    user.last_name = vk_user["last_name"]
                user.save()

            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user": UserSerializer(user, context={"request": request}).data})
        except requests.RequestException as e:
            return Response({"detail": f"Ошибка при обращении к VK API: {str(e)}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({"detail": f"Ошибка авторизации: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_serializer = UserSerializer(request.user, context={"request": request})
        return Response(user_serializer.data)


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related("content_type")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
