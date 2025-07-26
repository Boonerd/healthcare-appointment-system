from django.urls import path
from .views import TestAPI

urlpatterns = [path("test/", TestAPI.as_view(), name="test endpoint")]
