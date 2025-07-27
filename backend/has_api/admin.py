from django.contrib import admin
from .models import DoctorProfile, PatientProfile, User, AdminProfile

admin.site.register(User)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(AdminProfile)
