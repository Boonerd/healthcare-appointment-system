from django.contrib import admin
from .models import (
    User,
    DoctorProfile,
    PatientProfile,
    AdminProfile,
    Appointment,
)

admin.site.register(User)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(AdminProfile)
admin.site.register(Appointment)
