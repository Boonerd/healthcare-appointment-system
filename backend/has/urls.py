from django.contrib import admin
from django.urls import path, include

urlpatterns: list = [
    path("admin/", admin.site.urls),
    path("api/", include("has_api.urls")),
    path("api-auth/", include("rest_framework.urls")),
]
