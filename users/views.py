from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .game import GameManager
from .stats import StatManager
from .models import Checker, Player, AgentGroup
import json
from django.http import HttpResponse, JsonResponse
# Create your views here.
def home(request):
    param_value = request.GET.get('param')
    winners = StatManager.get_winner()
    match winners[0]:
        case 0:
            winner = None
        case 1:
            winner = winners[1].user.name
        case 2:
            winner = winners[1].group_name
        case _:
            winner = None
    
    
    context = {'param': param_value, 'kill_leaders': StatManager().get_kill_rankings(),
               'players_alive': StatManager().get_alive_players_count(), 'winner': winner}
    return render(request, "users/home.html", context)


#view that shows the assignemtn
def assignment(request):
    group_game = False
    current = Player.objects.get(pk=request.user.player.pk)
    try:
        if AgentGroup.objects.filter(players=current)[0].is_out == False:
            current_group = AgentGroup.objects.filter(players=current)[0]
            group_game = True
    except:
        pass


    if group_game:
        try:
            target = AgentGroup.objects.get(pk=current_group.target_group_pk)
        except AgentGroup.DoesNotExist:
            return redirect("/?param=noassignment")
        
        if target.is_out:
            GameManager.new_group_target(current_group, target)
        
        state = -1
        #possible states
        #your group is dead
        #you are dead but your group is not
        #you just killed someone


        #states_logic
        if current_group.is_out:
            pass
        return render(request, "users/group_assignment.html", context)
        #break is here right now
    if group_game == False:
        try:
            target = Player.objects.get(pk=current.target_pk)
        except Player.DoesNotExist:
            return redirect("/?param=noassignment")
        if target.is_dead:
            GameManager().new_target(request.user.player, target)
        
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
    
    
    gm = GameManager()
    if gm.win_condition() != 0:
        if current.is_winner:
            state = 3
        elif AgentGroup.objects.filter(players=current)[0].is_winner:
            state = 4
        
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
