from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserCreateViewSet,
                    UserReceiveTokenViewSet, UserViewSet)

v1_router = DefaultRouter()
v1_router.register("users", UserViewSet, basename="users")
v1_router.register("genres", GenreViewSet, basename="genres")
v1_router.register("categories", CategoryViewSet, basename="categories")
v1_router.register("titles", TitleViewSet, basename="titles")
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
v1_router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)

v1_auth_urls = [
    path(
        "signup/",
        UserCreateViewSet.as_view({"post": "create"}),
        name="signup"
    ),
    path(
        "token/",
        UserReceiveTokenViewSet.as_view({"post": "create"}),
        name="token",
    ),
]

urlpatterns = [
    path("v1/auth/", include(v1_auth_urls)),
    path("v1/", include(v1_router.urls)),
]
