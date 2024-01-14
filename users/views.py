from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .game import GameManager
from .models import Checker, Player
import json
from django.http import HttpResponse, JsonResponse
# Create your views here.
def home(request):
    param_value = request.GET.get('param')
    context = {'param': param_value}
    return render(request, "users/home.html", context)

#view that shows the assignemtn
def assignment(request):
    user_pk = request.user.pk
    state = -1

    # Check if there are any checkers with the current user as a target
    target_checkers = Checker.objects.filter(target__user__pk=user_pk, shown_to_target=False)

    # Check if there are any checkers with the current user as a killer
    killer_checkers = Checker.objects.filter(killer__user__pk=user_pk, shown_to_killer=False)

    # Function to handle checker logic
    def handle_checker(checker, result_attr, shown_attr):
        result = checker.checking()
        setattr(checker, result_attr, True)
        setattr(checker, shown_attr, True)
        checker.save()
        #checker.deletion()
        return result

    # Call checking() for each target instance and store the result
    target_checking_results = [handle_checker(target_checker, 'shown_to_target', 'shown_to_target') for target_checker in target_checkers]

    # Call checking() for each killer instance and store the result
    killer_checking_results = [handle_checker(killer_checker, 'shown_to_killer', 'shown_to_killer') for killer_checker in killer_checkers]

    gm = GameManager()
    if gm.win_condition():
        
        if request.user.player.is_winner:
            state = 3
    else:
        if any(target_checking_results):
            state = 2
        elif any(killer_checking_results):
            state = 1
        else:
            state = 0

    context = {'state': state}
    return render(request, "users/assignment.html", context)

def logout_view(request):
    logout(request)
    return redirect("/")


def handling(request):
    #make it users.player
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        param = data.get('param', None)

        user = request.user

        if param == "died":
            user.player.get_killed()
        
        elif param == "killed":
            user.player.kill_target()
        
        else:
            raise ValueError("wrong param")
        
        return HttpResponse('POST request processed succussfully')
    else:
        return JsonResponse({'error', 'Invalid request method'})
