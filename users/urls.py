from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path("", views.home, name='home'),
    path("assignment/", views.assignment, name="assignment"),
    path("logout/", views.logout_view, name='logout'),
    path("handling/", views.handling, name="handling"),
    path("complaints", views.submit_complaint, name='complaints'),
    path("rules/", views.rules, name='rules')
]