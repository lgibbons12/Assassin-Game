from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .game import GameManager
from .stats import StatManager
from .models import Checker, Player
import json
from django.http import HttpResponse, JsonResponse
# Create your views here.
def home(request):
    param_value = request.GET.get('param')
    winners = StatManager.get_winner()
    print(winners)
    
    print(winners)
    context = {'param': param_value, 'kill_leaders': StatManager().get_kill_rankings(),
               'players_alive': StatManager().get_alive_players_count(), 'winner': winners}
    return render(request, "users/home.html", context)


#view that shows the assignemtn
def assignment(request):
    
    try:
        target = Player.objects.get(pk=request.user.player.target_pk)
    except Player.DoesNotExist:
        return redirect("/?param=noassignment")
    if target.is_dead:
        GameManager().new_target(request.user.player, target)
    
    print(target.user.name)
    print(target.is_dead)
    user_pk = request.user.pk
    state = -1

    #get all unconfirmed checkers
    target_checkers = Checker.objects.filter(confirmations=2, action_performed=False)

    # Function to handle checker logic
    def handle_checker(checker):
        result = checker.checking()
        checker.action_performed = True
        checker.save()
        #checker.deletion()
        return result

    for checker in target_checkers:
        handle_checker(checker)
    
    current = Player.objects.get(pk=request.user.player.pk)
    gm = GameManager()
    if gm.win_condition():
        
        if current.is_winner:
            state = 3
    else:
        if current.is_dead:
            state = 2
        
        else:
            if current.in_waiting:
                return redirect(f'/?param=waiting')
            state = 0

    context = {'state': state}
    return render(request, "users/assignment.html", context)

def logout_view(request):
    logout(request)
    return redirect("/")


def submit_complaint(request):
    return render(request, "users/complaint.html")

def rules(request):
    return render(request, "users/rules.html")

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
        
        elif param == "discovered":
            user.player.discovered()
        
        elif param == "selfDefenseKilled":
            user.player.self_defense_killed()
        
        elif param == "selfDefenseDied":
            user.player.self_defense_died()
        else:
            raise ValueError("wrong param")
        
        user.player.in_waiting = True
        print(f"{user.name} is in waiting anymore")
        user.player.save()
        
        return HttpResponse('POST request processed succussfully')
    else:
        return JsonResponse({'error', 'Invalid request method'})
