from django.urls import path
from . import views
urlpatterns = [
    path("", views.home),
    path("assignment/", views.assignment),
    path("logout", views.logout_view)
]