#imports
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .game import GameManager
from .stats import StatManager
from .models import Checker, Player, AgentGroup, Game
import json
from django.http import HttpResponse, JsonResponse
from django.urls import reverse

from django.views.generic import ListView
from django.db.models import Q


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

    all_groups = AgentGroup.objects.all()

    # Filter groups where all players are dead
    
    for group in all_groups:
        # Count the number of dead players in the group
        dead_players_count = group.players.filter(is_dead=True).count()
        
        # If all players in the group are dead, add the group to the result
        if dead_players_count == group.players.count():
            group.is_out = True
            group.save()
    
    
    #change this if we implement new games
    current_game = Game.objects.all()[0]

    if current_game.state == 0:
        return redirect("users:assignment")
    elif current_game.state == 1:
        return redirect("users:group_assignment")

def group_assignment(request):
    #assignment for the groups
    current = Player.objects.get(pk=request.user.player.pk)

    try:
        current_group = AgentGroup.objects.filter(players=current)[0]
    except:
        return redirect(reverse('users:home'))
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
    
    try:
        return render(request, "users/group_assignment.html", context)
    except IndexError:
        return redirect(reverse('users:home'))
    except Exception as e:
    # Handle other exceptions
        return render(request, "error_template.html", {"error_message": str(e)})
    

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
    try:
        return render(request, "users/assignment.html", context)
    except IndexError:
        return redirect(reverse('users:home'))
    except Exception as e:
    # Handle other exceptions
        return render(request, "error_template.html", {"error_message": str(e)})



#page for group placement
def placement(request):
    new_team = request.GET.get("team_name")
    if new_team is not None:
        if len(AgentGroup.objects.filter(players=request.user.player)) == 0:
            new_group = AgentGroup.objects.create(group_name = new_team)
            new_group.players.add(request.user.player)
            new_group.save()

    player_added = request.GET.get("player_pk")
    if player_added is not None:
        current_group = AgentGroup.objects.filter(players=request.user.player)[0]
        current_group.players.add(Player.objects.get(pk=player_added))
        current_group.save()

    player_deleted = request.GET.get("player_cleared")
    if player_deleted is not None:
        current_group = AgentGroup.objects.filter(players=request.user.player)[0]
        current_group.players.remove(Player.objects.get(pk=player_deleted))
        current_group.save()

    is_placed = True
    current = request.user.player

    current_group = AgentGroup.objects.filter(players=current)
   
    if current_group == None or len(current_group) == 0:
        is_placed = False
        c_group = None
    else:
        c_group = current_group[0]
    
    all_players = Player.objects.all()

    #if there is a search
    search = request.GET.get('q')
    if search is not None:
        all_players = Player.objects.filter(Q(user__first_name__icontains=search) | Q(user__last_name__icontains=search)).order_by('user__last_name')

    players_not_on_team = [player for player in all_players if GameManager.player_on_team(player) is None]
    
    context = {'is_placed': is_placed, 'group': c_group, 'ggame': GameManager.is_placing_groups(), 'players': players_not_on_team, 'current_player': current}
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
