from .models import Player, AgentGroup
import random
class StatManager:

    @staticmethod
    def get_kill_rankings():
        # Return a list of top killers in descending order of kills
        return Player.objects.filter(is_playing=True).order_by('-kills')[:5]

    @staticmethod
    def get_alive_players_count():
        # Return the count of alive players
        count = Player.objects.filter(is_dead=False, is_playing = True).count()
        
        if count < 10:
            return 10
        elif count < 20:
            return 20
        elif count < 30:
            return 30
        else:
            return count
        
        
    
    @staticmethod
    def get_winner():
        player_winner = Player.objects.filter(is_winner=True)
        group_winner = AgentGroup.objects.filter(is_winner=True)
        returning = []
        if player_winner.count() == 1:
            returning.append(1)
            returning.append(player_winner[0])
        elif group_winner.count() == 1:
            returning.append(2)
            returning.append(group_winner[0])
        else:
            returning.append(0)
            returning.append(None)

        return returning
       