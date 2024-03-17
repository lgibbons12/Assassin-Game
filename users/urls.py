from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path("", views.home, name='home'),
    path("assignment/", views.assignment, name="assignment"),
    path("assignmentdirection/", views.assignment_direction, name='assignmentdirection'),
    path("groupassignment/", views.group_assignment, name='group_assignment'),
    path("placement/", views.placement, name='placement'),
    path("logout/", views.logout_view, name='logout'),
    path("handling/", views.handling, name="handling"),
    path("group_handling/", views.group_handling, name="group_handling"),
    path("complaints", views.submit_complaint, name='complaints'),
    path("rules/", views.rules, name='rules')
]