from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TestAPI,
    DBAPI,
    CustomTokenObtainPairView,
    UserRegisterView,
    UserDetailView,
    ActivateUserView,
    AppointmentViewSet,  # Make sure this exists in views.py
)

from rest_framework_simplejwt.views import TokenRefreshView

# Initialize DRF router for appointments
router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    # ✅ Test endpoints
    path("test/", TestAPI.as_view(), name="test-endpoint"),
    path("test/db", DBAPI.as_view(), name="db-test"),

    # ✅ Auth
    path("auth/register/", UserRegisterView.as_view(), name="user-register"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/me/", UserDetailView.as_view(), name="user-detail"),
    path("auth/activate/<str:national_id>/", ActivateUserView.as_view(), name="activate-user"),

    # ✅ Appointments API
    path("", include(router.urls)),
]
