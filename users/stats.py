from .models import Player

class StatManager:

    @staticmethod
    def get_kill_rankings():
        # Return a list of top killers in descending order of kills
        return Player.objects.filter(is_playing=True).order_by('-kills')[:5]

    @staticmethod
    def get_alive_players_count():
        # Return the count of alive players
        return Player.objects.filter(is_dead=False, is_playing = True).count()
    
    @staticmethod
    def get_winner():
        return Player.objects.filter(is_winner=True)[0]