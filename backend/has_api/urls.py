from django.urls import path
from .views import (
    TestAPI,
    DBAPI,
    CustomTokenObtainPairView,
    UserRegisterView,
    UserDetailView,
    ActivateUserView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("test/", TestAPI.as_view(), name="test endpoint"),
    path("test/db", DBAPI.as_view(), name="DB Test"),
    path("auth/register/", UserRegisterView.as_view(), name="user-register"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me/", UserDetailView.as_view(), name="user-detail"),
    path(
        "auth/activate/<str:national_id>/",
        ActivateUserView.as_view(),
        name="activate-users",
    ),
]
