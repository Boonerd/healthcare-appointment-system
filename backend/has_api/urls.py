from django.urls import path
from .views import (
    TestAPI,
    DBAPI,
    CustomTokenObtainPairView,
    UserRegisterView,
    UserDetailView,
    ActivateUserView,
    DoctorListView,
    CreateAppointmentView,
    MyAppointmentsView,
    CancelAppointmentView,
    DoctorAvailabilityView,
    PatientListView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("test/", TestAPI.as_view(), name="test endpoint"),
    path("test/db/", DBAPI.as_view(), name="DB Test"),
    path("auth/register/", UserRegisterView.as_view(), name="user-register"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me/", UserDetailView.as_view(), name="user-detail"),
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
]
