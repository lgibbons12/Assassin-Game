from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .game import GameManager
from .models import Checker
# Create your views here.
def home(request):
    return render(request, "users/home.html")

#view that shows the assignemtn
def assignment(request):
    #states
    #state 0 is nothing, state 1 is they killed someone, state 2 is they were killed
    user_pk = request.user.pk

    # Check if there are any checkers with the current user as a target
    target_checkers = Checker.objects.filter(target__user__pk=user_pk, shown_to_target = False)

    

    # Check if there are any checkers with the current user as a killer
    killer_checkers = Checker.objects.filter(killer__user__pk=user_pk, shown_to_killer = False)

    # Variable to store the results of checking for each target and killer instance
    target_checking_results = []
    killer_checking_results = []

    # Call checking() for each target instance and store the result
    for target_checker in target_checkers:
        result = target_checker.checking()
        if result:
            target_checker.shown_to_target = True
            
            target_checker.save()
            target_checker.deletion()
        target_checking_results.append(result)
    
    

    # Call checking() for each killer instance and store the result
    for killer_checker in killer_checkers:
        result = killer_checker.checking()
        if result:
            killer_checker.shown_to_killer = True
            killer_checker.save()
            killer_checker.deletion()
        killer_checking_results.append(result)

    if True in target_checking_results:
        state = 2
    elif True in killer_checking_results:
        state = 1
    else:
        state = 0
    context = {
        'state':state,
    }

    return render(request, "users/assignment.html", context)

def logout_view(request):
    logout(request)
    return redirect("/")