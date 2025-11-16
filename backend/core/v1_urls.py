from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.views import FavoriteViewSet, LoginView, LogoutView, MeView, RegisterView, VKLoginView
from assistant.views import QueryAssistantView
from events.views import EventViewSet
from knowledge.views import MaterialCategoryViewSet, MaterialViewSet
from locations.views import ActivityCategoryViewSet, CityViewSet
from news.views import NewsItemViewSet
from organizations.views import OrganizationViewSet

router = DefaultRouter()
router.register("cities", CityViewSet, basename="city")
router.register("activity-categories", ActivityCategoryViewSet, basename="activity-category")
router.register("materials", MaterialViewSet, basename="material")
router.register("material-categories", MaterialCategoryViewSet, basename="material-category")
router.register("organizations", OrganizationViewSet, basename="organization")
router.register("events", EventViewSet, basename="event")
router.register("news", NewsItemViewSet, basename="news")
router.register("favorites", FavoriteViewSet, basename="favorite")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/vk/", VKLoginView.as_view(), name="auth-vk"),
    path("auth/logout/", LogoutView.as_view(), name="auth-logout"),
    path("auth/me/", MeView.as_view(), name="auth-me"),
    path("assistant/query/", QueryAssistantView.as_view(), name="assistant-query"),
]

