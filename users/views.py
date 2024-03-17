#imports
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .game import GameManager
from .stats import StatManager
from .models import Checker, Player, AgentGroup, Game
import json
from django.http import HttpResponse, JsonResponse


# Create your views here.
def home(request):
    #get the parameter value to know what waiting message to show after actions
    param_value = request.GET.get('param')

    #winner to check if there is a winner
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
    
    
    #grab info to display in home.html
    context = {'param': param_value, 'kill_leaders': StatManager().get_kill_rankings(),
               'players_alive': StatManager().get_alive_players_count(), 'winner': winner, 'ggame': GameManager.is_placing_groups()}
    return render(request, "users/home.html", context)

#takes in the get assignment button
#handles checking for kills
#directs users to group or individual pages based on the game being played
def assignment_direction(request):
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
    
    #change this if we implement new games
    current_game = Game.objects.all()[0]

    if current_game.state == 0:
        return redirect("users:assignment")
    elif current_game.state == 1:
        return redirect("users:group_assignment")

def group_assignment(request):
    #assignment for the groups
    current = Player.objects.get(pk=request.user.player.pk)
    current_group = AgentGroup.objects.filter(players=current)[0]
    state = -1

    #if our group is not out call the group, otherwise state is 1 for them dead
    if AgentGroup.objects.filter(players=current)[0].is_out == False:
            current_group = AgentGroup.objects.filter(players=current)[0]
    else:
        state = 1
    
    try:
        target_group = AgentGroup.objects.get(pk=current_group.target_group_pk)
    except AgentGroup.DoesNotExist:
            return redirect("/?param=noassignment")
    
    #get new target group if users is out
    if target_group.is_out:
        GameManager.new_group_target(current_group, target_group)
    
    
    if state != 2:
        if current.is_dead:
            state = 2
        elif GameManager.win_condition() != 0:
            if current_group.is_winner:
                state = 3
        elif current.in_waiting:
            return redirect(f'/?param=waiting')
        else:
            state = 0


    #see if we need tro display extra info
    player_was_killed = Checker.objects.filter(confirmations__lt=2, action_performed=False, target=current).first()
    
    
    player_killed_sd = Checker.objects.filter(confirmations__lt=2, action_performed=False, killer=current).first()

    
    #states
    #-1 is null, 0 is normal, 1 is group died, 2 is you died, 3 is your group won
    target_group = AgentGroup.objects.get(pk=current_group.target_group_pk)
    context = {'state': state, 'team': current_group, 't_group': target_group, 'pwk': player_was_killed, 'pksd': player_killed_sd, 'ggame': GameManager.is_placing_groups()}
    return render(request, "users/group_assignment.html", context)

#view that shows the assignemtn
def assignment(request):
    
    current = Player.objects.get(pk=request.user.player.pk)
    

    try:
        target = Player.objects.get(pk=current.target_pk)
    except Player.DoesNotExist:
        return redirect("/?param=noassignment")
    if target.is_dead:
        GameManager().new_target(request.user.player, target)
    
    user_pk = request.user.pk
    state = -1
    
   


    gm = GameManager()
    if gm.win_condition() != 0:
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



#page for group placement
def placement(request):
    is_placed = True
    current = request.user.player

    current_group = AgentGroup.objects.filter(players=current)
   
    if current_group == None or len(current_group) == 0:
        is_placed = False
    

    
    context = {'is_placed': is_placed, 'group': current_group[0], 'ggame': GameManager.is_placing_groups()}
    return render(request, "users/placement.html", context)




def logout_view(request):
    logout(request)
    return redirect("/")


def submit_complaint(request):
    context = {'ggame': GameManager.is_placing_groups()}
    return render(request, "users/complaint.html", context)

def rules(request):
    context = {'ggame': GameManager.is_placing_groups()}
    return render(request, "users/rules.html", context)

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


def group_handling(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        param = data.get('param', None)
        who_pk = data.get('who_pk', None)


        user = request.user

        if param == "died":
            user.player.get_killed()
        
        elif param == "killed":
            user.player.kill_target(who = who_pk)
        
        elif param == "discovered":
            user.player.discovered()
        
        elif param == "selfDefenseKilled":
            user.player.self_defense_killed()
        
        elif param == "selfDefenseDied":
            user.player.self_defense_died(who=who_pk)
        else:
            raise ValueError("wrong param")
        
        user.player.in_waiting = True
        print(f"{user.name} is in waiting anymore")
        user.player.save()
        
        return HttpResponse('POST request processed succussfully')
    else:
        return JsonResponse({'error', 'Invalid request method'})
