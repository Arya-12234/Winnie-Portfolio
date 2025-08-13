from .views import index, contact
from django.urls import path

urlpatterns = [
    path("", index),
    path("contact", contact),
]