from django.shortcuts import render, redirect
from django.contrib.auth import logout


# Create your views here.
def home(request):
    return render(request, "users/home.html")

#view that shows the assignemtn
def assignment(request):
    return render(request, "users/assignment.html")

def logout_view(request):
    logout(request)
    return redirect("/")