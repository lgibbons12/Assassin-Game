from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .game import GameManager

# Create your views here.
def home(request):
    return render(request, "users/home.html")

#view that shows the assignemtn
def assignment(request):
    gm = GameManager()
    gm.assign_targets()
    return render(request, "users/assignment.html")

def logout_view(request):
    logout(request)
    return redirect("/")