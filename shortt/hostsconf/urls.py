from django.urls import path
from django.contrib import admin
from .views import wildcard_redirect

urlpatterns = [
    path('', wildcard_redirect),
]
