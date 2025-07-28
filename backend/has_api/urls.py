from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TestAPI,
    DBAPI,
    CustomTokenObtainPairView,
    UserRegisterView,
    UserDetailView,
    ActivateUserView,
<<<<<<< Updated upstream
    AppointmentViewSet,  # Make sure this exists in views.py
=======
    DoctorListView,
    CreateAppointmentView,
    MyAppointmentsView,
    CancelAppointmentView,
    DoctorAvailabilityView,
    PatientListView,
>>>>>>> Stashed changes
)

from rest_framework_simplejwt.views import TokenRefreshView

# Initialize DRF router for appointments
router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
<<<<<<< Updated upstream
    # ✅ Test endpoints
    path("test/", TestAPI.as_view(), name="test-endpoint"),
    path("test/db", DBAPI.as_view(), name="db-test"),

    # ✅ Auth
=======
    path("test/", TestAPI.as_view(), name="test endpoint"),
    path("test/db/", DBAPI.as_view(), name="DB Test"),
>>>>>>> Stashed changes
    path("auth/register/", UserRegisterView.as_view(), name="user-register"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/me/", UserDetailView.as_view(), name="user-detail"),
<<<<<<< Updated upstream
    path("auth/activate/<str:national_id>/", ActivateUserView.as_view(), name="activate-user"),

    # ✅ Appointments API
    path("", include(router.urls)),
=======
    path(
        "auth/activate/<str:national_id>/",
        ActivateUserView.as_view(),
        name="activate-users",
    ),
    path("doctors/", DoctorListView.as_view(), name="view doctors"),
    path("patients/", PatientListView.as_view(), name="view patients"),
    path(
        "appointments/create/",
        CreateAppointmentView.as_view(),
        name="create-appointment",
    ),
    path("appointments/me/", MyAppointmentsView.as_view(), name="my-appointments"),
    path(
        "appointments/cancel/<int:appointment_id>/",
        CancelAppointmentView.as_view(),
        name="cancel-appointment",
    ),
    path(
        "doctor-availability/",
        DoctorAvailabilityView.as_view(),
        name="doctor availability",
    ),
>>>>>>> Stashed changes
]
